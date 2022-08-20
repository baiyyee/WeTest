import os
import pytest
import logging
import pandas as pd
from pathlib import Path
from WeTest.util import testdata
from WeTest.util.client import DataBase, RabbitMQ, SSH, SFTP, Hive, S3


def test_create_table(sqlite_in_memory: DataBase):

    sql = "create table if not exists users (name varchar(20), age int, gender varchar(5))"

    sqlite_in_memory.exec_sql(sql)


def test_insert(sqlite_in_memory: DataBase):

    sql = "insert into users (name, age, gender) VALUES (:name, :age, :gender)"

    params = {
        "name": testdata.name(),
        "age": testdata.int(18, 30),
        "gender": testdata.gender(),
    }

    sqlite_in_memory.exec_sql(sql, params)


def test_bulk_insert(sqlite_in_memory: DataBase):

    sql = "insert into users (name, age, gender) VALUES (:name, :age, :gender)"

    params = [
        {
            "name": testdata.name(),
            "age": testdata.int(18, 30),
            "gender": testdata.gender(),
        },
        {
            "name": testdata.name(),
            "age": testdata.int(18, 30),
            "gender": testdata.gender(),
        },
    ]

    sqlite_in_memory.exec_sql(sql, params)


def test_df_to_db(sqlite_in_memory: DataBase):

    data = [
        {
            "name": testdata.name(),
            "age": testdata.int(18, 30),
            "gender": testdata.gender(),
        },
        {
            "name": testdata.name(),
            "age": testdata.int(18, 30),
            "gender": testdata.gender(),
        },
    ]

    df = pd.DataFrame(data)

    sqlite_in_memory.df_to_db(df, "users")


def test_query(sqlite_in_memory: DataBase):

    sql = "select * from users"

    result = sqlite_in_memory.exec_sql(sql)

    for row in result:
        logging.info(row)


def test_query_to_df(sqlite_in_memory: DataBase):

    sql = "select * from users"

    result = sqlite_in_memory.query_to_df(sql)

    logging.info(result)


def test_query_to_dict(sqlite_in_memory: DataBase):

    sql = "select * from users"

    result = sqlite_in_memory.query_to_dict(sql)

    logging.info(result)


def test_delete(sqlite_in_memory: DataBase):

    sql = "delete from users where age >= 18"

    sqlite_in_memory.exec_sql(sql)


@pytest.mark.skip
def test_read(s3: S3):

    bucket_name = "bucket"
    s3_path = r"test/test.txt"

    content = s3.read_file(bucket_name, s3_path)

    assert content == "upload to s3"


@pytest.mark.skip
def test_download_file(s3: S3, tmp_path: Path):

    bucket_name = "bucket"
    s3_path = r"test/test.txt"
    local_path = str(tmp_path / "uploadfile.txt")

    s3.download_file(bucket_name, s3_path, local_path)

    logging.info(f"Download to: {local_path}")

    with open(local_path, "r") as f:
        content = f.read()
        assert content == "upload to s3"


@pytest.mark.skip
def test_download_folder(s3: S3, tmp_path: Path):

    bucket_name = "bucket"
    local_path = str(tmp_path)
    s3_path = r"DAILY/20200818"

    s3.download_folder(bucket_name, s3_path, local_path)

    logging.info(f"Download to: {local_path}")
    logging.info(os.listdir(local_path))


@pytest.mark.skip
def test_upload(s3: S3):

    bucket_name = "bucket"
    local_path = r"data/uploadfile.txt"
    s3_path = r"test/test_uploadfile.txt"

    s3.upload_file(bucket_name, s3_path, local_path)

    content = s3.read_file(bucket_name, s3_path)

    assert content == "upload to s3"


@pytest.mark.skip
def test_read_file(sftp: SFTP):

    lines = sftp.read_file("/tmp/test.txt")

    for line in lines:
        logging.info(line, end="")


@pytest.mark.skip
def test_append_file(sftp: SFTP):

    sftp.write_file("/tmp/logs/test.log", ["a\nb", "c\nb"])


@pytest.mark.skip
def test_write_file(sftp: SFTP):

    sftp.write_file("/tmp/logs/test.log", ["a\nb", "c\nb"], mode="w")


@pytest.mark.skip
def test_list_dir(sftp: SFTP):

    lines = sftp.list_dir("/tmp")

    for line in lines:
        logging.info(line)


@pytest.mark.skip
def test_download(sftp: SFTP, tmp_path: Path):

    path = str(tmp_path / "test.log")

    sftp.download("/tmp/logs/test.log", path)

    logging.info(f"Download to: {path}")


@pytest.mark.skip
def test_ssh_exec(ssh: SSH):

    cmd = "ls"
    stdout, stderr = ssh.run(cmd)

    for line in stdout:
        logging.info(line)


@pytest.mark.skip
def test_get_nacos_config(config):

    assert config["tracker"]["host"] == ""

    logging.info(config)


@pytest.mark.skip
def test_query_as_dict(hive: Hive):

    sql = "select * from table where date = '20200827' order by timestamp"

    result = hive.query_as_dict(sql)

    logging.info(result)

    assert result is not None


@pytest.mark.skip
def test_query_as_df(hive: Hive):

    sql = "select * from table where date = '20200827' order by timestamp"

    result = hive.query_as_df(sql)

    logging.info(result)

    assert result is not None


@pytest.mark.skip
def test_create_partition(hive: Hive):

    dates = ["20200921"]

    for date in dates:
        sqls = ["ALTER TABLE db.table ADD IF NOT EXISTS PARTITION (project='PROJECT',date='{}',type='type',section='section')"]

        for sql in sqls:
            result = hive.exec_sql(sql.format(date))
            logging.info(result)


@pytest.mark.skip
def test_rabbitmq(rabbitmq: RabbitMQ):

    message = {
        "uuid": "f1228139-3bc4-4821-856b-1be837bcabf2",
        "email": "test@test.com",
        "name": "username",
        "path": "bucket/testdata.csv",
        "timestamp": "1652357385709",
    }

    rabbitmq.send_message("mq_queue", message)
