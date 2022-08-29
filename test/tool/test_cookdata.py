import pytest
import logging
from WeTest.util import testdata
from WeTest.tool import cookdata
from WeTest.util.client import DataBase


def test_cook_df_data():

    seeds = {
        "id": "{{str(data.int(1,100)).zfill(5)}}",
        "name": "{{data.name()}}",
        "gender": "{{data.gender()}}",
        "address": "{{data.address()}}",
        "birthday": "{{data.date_between('20210101', '20211231')}}",
    }
    
    df = cookdata.cook_df_data(seeds, None, count=10)
    
    logging.info(df)


@pytest.mark.skip
def test_create_table(mysql: DataBase):

    # Note: auto_increment syntax is not support in sqlite
    sql = "create table if not exists users (id int primary key auto_increment not null, name varchar(20), age int, gender varchar(5), tel varchar(11), brithday date, created datetime)"

    mysql.exec_sql(sql)


@pytest.mark.skip
def test_cook_db_data(mysql: DataBase):

    tables = ["users"]

    macro = [
        ("{{gender}}", "male"),
        ("{{age}}", 18),
    ]

    seeds = {
        "name": testdata.name(),
        "height": testdata.int(150, 180),
        "tel": testdata.phone(),
    }
    
    cookdata.cook_db_data(mysql, tables, macro, seeds, 5)
 

@pytest.mark.skip
def test_query(mysql: DataBase):

    sql = "select * from users"

    result = mysql.exec_sql(sql)

    for row in result:
        logging.info(row)