import os
import re
import logging
import numpy as np
import pandas as pd
from . import date, encry
from functools import reduce
from . import testdata as data
from openpyxl.utils import get_column_letter
from pandas import DataFrame, Series, ExcelWriter, ExcelFile


def dict_to_df(json: dict) -> DataFrame:

    return DataFrame([json])


def df_to_dict(df: DataFrame) -> dict:

    data = []
    if not df.empty:
        headers = list(df.columns.values)

        for index in df.index.values:
            row = df.loc[index, headers].to_dict()
            data.append(row)

    return data


def cross_df(df_list: list) -> DataFrame:

    return reduce(lambda left, right: left.merge(right, how="cross"), df_list)


def df_append_series(df: DataFrame, series: Series) -> DataFrame:

    series = DataFrame([series.to_dict()])
    series = series.reindex(np.repeat(series.index.values, len(df)), method="ffill").reset_index(drop=True)

    return pd.concat([df, series], axis=1)


def read_excel_to_df(path: str, sheet: str) -> DataFrame:

    df = pd.read_excel(path, sheet, dtype=str)
    df.fillna("", inplace=True)

    return df


def read_excel_to_dict(path: str, sheet: str) -> dict:

    df = read_excel_to_df(path, sheet)
    data = df_to_dict(df)

    return data


def read_excel_by_sheets(path: str, sheets: list = None) -> dict:

    sheets = sheets if sheets else ExcelFile(path).sheet_names

    data = {}
    for sheet in sheets:
        data[sheet] = read_excel_to_dict(path=path, sheet=sheet)

    return data


def df_to_csv(df: DataFrame, path: str = None, mode: str = "w", encoding:str = "utf-8"):

    df.to_csv(path, index=False, mode=mode, encoding=encoding)
    
    logging.info(f"Save file to: {path}")
    
    return path


def df_to_excel(df: DataFrame, path: str, sheet: str, mode: str = "w", **kwargs) -> str:

    # Note: if_sheet_exists is only valid in append mode (mode='a')
    if mode.lower() == "a":
        kwargs.setdefault("if_sheet_exists", "overlay")

    with ExcelWriter(path, mode=mode, engine="openpyxl", **kwargs) as writer:
        df.to_excel(writer, sheet_name=sheet, index=False, encoding="utf-8")

        # auto fit column width
        for index, column in enumerate(df.columns):
            width = max(df[column].astype(str).map(len).max(), len(column))
            writer.sheets[sheet].column_dimensions[get_column_letter(index + 1)].width = width + 2

        writer.save()

    logging.info(f"Save file to: {path}")

    return path


def df_append_excel(df: DataFrame, path: str, sheet: str):

    df_ori = read_excel_to_df(path, sheet)

    df = pd.concat([df_ori, df], ignore_index=True)

    return df_to_excel(df, path, sheet, mode="a")


def replace_macro_output(
    source: str, macro: list, drop_columns: list = None, target: str = None, sheet: str=None, mode: str = "w"
):

    datas = read_excel_to_dict(source, sheet)

    temp = []
    for data in datas:
        _, kw = replace_macro(macro, None, **data)
        temp += [kw]

    df = DataFrame(temp)

    if drop_columns:
        df.drop(columns=drop_columns, axis=1, inplace=True)

    target = source.replace(".xlsx", "_replaced.xlsx") if target is None else target

    if ".csv" in target:
        df_to_csv(df, target, mode, encoding="utf-8")

    else:
        if os.path.exists(target) and mode.lower() == "a":
            df_append_excel(df, target, sheet)
        else:
            df.to_excel(target, sheet_name=sheet, index=False, encoding="utf-8")

        logging.info(f"Save file to: {target}")

    return target


def str_to_bool(string: str) -> bool:

    if string.lower() in ["true", "yes", "y", "1"]:
        return True

    elif string.lower() in ["false", "no", "n", "0"]:
        return False


def unpack_dict(data: dict) -> dict:
    def expand_dict(data):
        for key, value in data.items():
            if isinstance(value, dict):
                for k, v in expand_dict(value):
                    yield (k, v)
            else:
                yield (key, value)

    data = {k: v for k, v in expand_dict(data)}

    return data


def replace_macro(macro: list, *args, **kwargs) -> tuple:

    macro_pattern = r"{{.*?}}"
    method_pattern = r"\(.*\)"

    if macro is None:
        macro = [(None, None)]

    if args:
        args = list(args)

        for index in range(len(args)):
            original = args[index]

            if re.search(macro_pattern, str(original)):
                matches = re.findall(macro_pattern, str(original))

                for match in matches:
                    original = args[index]
                    replaced = "default"

                    if re.search(method_pattern, str(match)):
                        try:
                            replaced = eval("{}".format(match.replace("{{", "").replace("}}", "")))

                        except NameError as e:
                            logging.error("Invalid Module Or Method! Exception Details: {}".format(e))
                    else:

                        for ori, new in macro:
                            if ori == match:
                                replaced = new

                    if replaced == "default":
                        pass

                    elif replaced or replaced == 0:
                        args[index] = original.replace(match, str(replaced))

                    elif replaced is None:
                        args[index] = original.replace(match, "")

        args = tuple(args)

    if kwargs:
        for key, value in kwargs.items():
            original = value

            if re.search(macro_pattern, str(original)):
                matches = re.findall(macro_pattern, str(original))

                for match in matches:
                    replaced = "default"

                    if re.search(method_pattern, str(match)):
                        try:
                            replaced = eval("{}".format(match.replace("{{", "").replace("}}", "")))

                        except NameError as e:
                            logging.error("Invalid Module Or Method! Exception Details: {}".format(e))

                    else:
                        for ori, new in macro:
                            if ori == match:
                                replaced = new

                    if replaced == "default":
                        pass

                    elif replaced or replaced == 0:
                        kwargs[key] = value.replace(match, str(replaced))
                        value = kwargs[key]

                    elif replaced is None or replaced == "":
                        kwargs[key] = value.replace(match, "")
                        value = kwargs[key]

    return args, kwargs
