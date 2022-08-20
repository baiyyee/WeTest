import re
import logging
from pandas import DataFrame
from WeTest.util.client import DataBase
from WeTest.util import provider, testdata


def cook_df_data(seeds: dict, macro: list, count: int=1) -> DataFrame:

    data = []
    for _ in range(0, count):
        _, kw = provider.replace_macro(macro, None, **seeds)
        data.append(kw)

    return DataFrame(data)


def cook_db_data(database: DataBase, tables: list, macro: list, seeds: dict, count: int):
    
    pattern = r"\d+"
    
    for table in tables:
        sql_desc = f"desc {table}"

        df = database.query_to_df(sql_desc)

        params = ", ".join([f":{value}" for value in df["Field"].tolist()])
        sql_insert = f"insert into {table} values ({params})"

        datas = []
        for _ in range(0, count):
            data = {}
            
            for _, row in df.iterrows():
                
                if row["Extra"] == "auto_increment":
                    data[row["Field"]] = ""

                elif row["Field"] in seeds:
                    data[row["Field"]] = seeds[row["Field"]]
                                        
                elif "char" in row["Type"]:
                    length = int(re.findall(pattern, row["Field"])[0])
                    data[row["Field"]] = testdata.string(min=1, max=length)
                    
                elif "date" in row["Type"]:
                    data[row["Field"]] = testdata.datetime("%Y-%m-%d")
                    
                elif "datetime" in row["Type"]:
                    data[row["Field"]] = testdata.datetime("%Y-%m-%d %H:%M:%S")
                    
                else:
                    data[row["Field"]] = "{{field}}".format(field = row["Field"])

            _, kw = macro.replace_macro(macro, None, **data)
            
            datas.append(kw)

        database.exec_sql(sql_insert, datas)
        
        logging.info(f"Insert {table} OK, {count} row affected.")