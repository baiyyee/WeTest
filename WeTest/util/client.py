import os
import pika
import json
import boto3
import logging
import paramiko
import requests
import pandas as pd
from jira import JIRA
from requests import Session
from pandas import DataFrame
from paramiko import SFTPFile
from .config import read_yaml
from impala.dbapi import connect
from impala.util import as_pandas
from botocore.config import Config
from sqlalchemy import text, create_engine


class DataBase:
    def __init__(
        self, database: str, username: str = None, password: str = None, host: str = None, port: int = None, type="mysql"
    ):

        url = None

        if type.lower() == "mysql":
            url = "mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, database)

        elif type.lower() == "sqlite":
            # In case someone gets here again after being greeted by that error, the valid SQLite URL forms are any one of the following:
            #   sqlite:///:memory: (or, sqlite://)
            #   sqlite:///relative/path/to/file.db
            #   sqlite:////absolute/path/to/file.db

            url = "sqlite+pysqlite:///{}".format(database)

        elif type.lower() == "postgresql":
            url = "postgresql://{}:{}@{}:{}/{}".format(username, password, host, port, database)

        elif type.lower() == "oracle":
            url = "oracle://{}:{}@{}:{}/{}".format(username, password, host, port, database)

        elif type.lower() == "mssql":
            url = "mssql+pymysql://{}:{}@{}:{}/{}".format(username, password, host, port, database)

        self.engine = create_engine(url, encoding="utf8", echo=False)
        
        self.connect = self.engine.connect()
        

    def exec_sql(self, sql: str, params=None):
        
        return self.connect.execute(text(sql), params)

    def query_to_dict(self, sql: str, params=None) -> dict:

        return self.exec_sql(sql, params).mappings().all()

    def query_to_df(self, sql: str) -> DataFrame:

        return pd.read_sql(sql, self.engine)

    def df_to_db(self, dataframe: DataFrame, table: str):

        return dataframe.to_sql(table, self.engine, if_exists="append", index=False)
    
    def close(self):
        self.connect.close()


class RabbitMQ:
    def connect(self, host: str, port: str, vhost: str, username: str, password: str):

        credentials = pika.PlainCredentials(username, password)

        connect = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port, credentials=credentials, virtual_host=vhost, heartbeat=600, blocked_connection_timeout=300
            )
        )

        self.connect = connect

    def publish_message(self, queue: str, body: dict):

        channel = self.connect.channel()
        channel.queue_declare(queue=queue, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(body),
            properties=pika.BasicProperties(content_type="application/json"),
        )

        logging.info("queue: {}".format(queue))
        logging.info("body : {}".format(body))


class SFTP:
    def connect(self, host: str, port: str, username: str, password: str):

        transport = paramiko.Transport(sock=(host, port))
        transport.connect(username=username, password=password)

        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def read_file(self, path: str) -> SFTPFile:

        return self.sftp.file(path, "r", -1)

    def write_file(self, path: str, content: str, mode: str = "a"):

        file = self.sftp.file(path, mode, -1)
        file.writelines(content)
        file.flush()

    def list_dir(self, path: str) -> list:

        return self.sftp.listdir(path)

    def upload(self, source: str, target: str):

        self.sftp.put(source, target)

    def download(self, source: str, target: str):

        self.sftp.get(source, target)

    def close(self):

        self.sftp.close()


class SSH:
    def connect(self, host: str, port: str, username: str, password: str):

        ssh = paramiko.SSHClient()
        known_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(known_host)
        ssh.connect(host, port, username, password)

        self.ssh = ssh

    def exec(self, command: str) -> tuple:

        logging.info(f"run cmd: {command}")

        stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)

        for line in iter(stdout.readline, ""):
            logging.info(line.rstrip())

        return stdout, stderr

    def close(self):

        self.ssh.close()


class Nacos:
    def connect(self, host: str, username: str, password: str):

        self.host = host
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None

    def get_token(self) -> str:

        if self.token:
            return self.token

        url = self.host + "/nacos/v1/auth/users/login"

        data = {"username": self.username, "password": self.password}
        response = self.session.post(url, data=data)

        self.token = response.json()["accessToken"]

        return self.token

    def get_config(self, tenant: str, data_id: str, group: str) -> dict:

        url = self.host + "/nacos/v1/cs/configs"

        self.token = self.get_token()

        params = {"tenant": tenant, "dataId": data_id, "group": group, "accessToken": self.token}
        response = self.session.get(url, params=params)
        config = read_yaml(response.text, type="string")

        return config


class S3:
    def connect(self, aws_access_key_id: str, aws_secret_access_key: str, endpoint: str):

        config = Config(signature_version="s3")

        self.s3 = boto3.resource(
            service_name="s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint,
            region_name="cn-north-1",
            config=config,
        )

    def read_file(self, bucket: str, path: str) -> str:

        return self.s3.Object(bucket, path).get()["Body"].read().decode("utf-8").strip("\n")

    def download_file(self, bucket: str, source: str, target: str):

        self.s3.Object(bucket, source).download_file(target)

    def download_folder(self, bucket: str, source: str, target: str):

        temp = target
        bucket = self.s3.Bucket(bucket)
        for obj in bucket.objects.filter(Prefix=source):
            target = os.path.join(temp, obj.key)
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            bucket.download_file(obj.key, target)

    def upload_file(self, bucket: str, source: str, target: str):
        self.s3.Object(bucket, source).upload_file(target)


class Hive:
    def connect(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        auth_mechanism: str,
        database: str,
    ):

        self.connect = connect(
            host=host, port=port, user=user, password=password, auth_mechanism=auth_mechanism, database=database
        )

    def exec_sql(self, sql: str):

        cursor = self.connect.cursor()
        cursor.execute(sql)
        return cursor

    def query_as_df(self, sql: str) -> DataFrame:

        cursor = self.exec_sql(sql)
        df = as_pandas(cursor)
        return df

    def query_as_dict(self, sql: str) -> dict:

        df = self.query_as_df(sql)

        data = []
        if not df.empty:
            headers = list(df.columns.values)
            for index in df.index.values:
                row = df.loc[index, headers].to_dict()
                data.append(row)

        return data


class Jira:
    def __init__(self, server: str, username: str, password: str) -> JIRA:

        return JIRA(basic_auth=(username, password), server=server)


class Confluence:
    def __init__(self, server: str, username: str, password: str) -> Session:

        data = {"os_username": username, "os_password": password}

        session = Session()
        session.post(server, data=data)

        return session
