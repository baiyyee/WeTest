import os
import pytest
import logging
import numpy as np
from pathlib import Path
from pandas import DataFrame, Series
from WeTest.util import provider, compare, testdata


testdata = {"path": ""}


def test_testdata(tmp_path: Path):

    path = str(tmp_path / "test_exceldata.xlsx")

    sheet01 = [
        {"name": "Silence", "age": 31, "gender": "male", "height": 180},
        {"name": "Hone", "age": 18, "gender": "female", "height": 165},
    ]

    sheet02 = [
        {"age": 31, "gender": "male", "height": 180},
        {"age": 18, "gender": "female", "height": 165},
    ]

    df01 = DataFrame(sheet01)
    df02 = DataFrame(sheet02)

    provider.df_to_excel(df01, path, "Sheet1")
    provider.df_to_excel(df02, path, "Sheet2", "a")

    testdata["path"] = path


def test_dict_to_df():

    data = {"name": "Silence", "age": 31, "gender": "male", "height": 180}

    df = provider.dict_to_df(data)

    assert isinstance(df, DataFrame) == True
    assert df["name"][0] == "Silence"


def test_df_to_dict():

    data = {"name": "Silence", "age": 31, "gender": "male", "height": 180}

    df = provider.dict_to_df(data)
    data = provider.df_to_dict(df)

    assert isinstance(data[0], dict) == True
    assert data[0]["name"] == "Silence"


def test_cross_df():

    data1 = [
        {"name": "Silence", "age": 31, "gender": "male", "height": 180},
        {"name": "Hone", "age": 18, "gender": "female", "height": 165},
    ]
    data2 = [
        {"country": "China", "province": "Hubei", "city": "huanggang"},
        {"country": "China", "province": "Hubei", "city": "wuhan"},
    ]

    df1 = DataFrame(data1)
    df2 = DataFrame(data2)

    cross_df = provider.cross_df([df1, df2])

    assert isinstance(cross_df, DataFrame) == True
    assert cross_df.shape == (4, 7)


def test_df_append_series():

    data1 = [{"name": "hhb", "age": 18}, {"name": "huabo", "age": 18}]
    data2 = {"height": 180, "weight": 60}
    expect = [{"name": "hhb", "age": 18, "height": 180, "weight": 60}, {"name": "huabo", "age": 18, "height": 180, "weight": 60}]

    df1 = DataFrame(data1)
    df2 = Series(data2)
    expect_df = DataFrame(expect)

    actual_df = provider.df_append_series(df1, df2)

    result = compare.campare_df(actual_df, expect_df, "name")

    assert result == True


def test_read_excel_to_df():

    data = provider.read_excel_to_df(testdata["path"], 0)

    assert isinstance(data, DataFrame) == True
    assert data["age"][0] == "31"


def test_read_excel_to_dict():

    data01 = provider.read_excel_to_dict(testdata["path"], 0)[0]
    data02 = provider.read_excel_to_dict(testdata["path"], "Sheet1")

    payload = """
    {{
        "gender": "{gender}",
        "height": "180",
        "others": [
            {{
            "age": "{age}",
            "tel": "11111111111",
            "others": [
                {{
                    "x": "a"
                }}
            ]
            }}
        ]
    }}
    """

    payload = payload.format(**data01)

    logging.info(payload)

    assert data02[-1]["age"] == "18"
    assert data02[-1]["gender"] == "female"


def test_read_excel_by_sheets_specific():

    data = provider.read_excel_by_sheets(testdata["path"], ["Sheet1", "Sheet2"])

    assert data["Sheet1"][0]["age"] == "31"
    assert data["Sheet2"][-1]["age"] == "18"


def test_read_excel_by_sheets_all():

    data = provider.read_excel_by_sheets(testdata["path"])

    assert data["Sheet1"][0]["age"] == "31"
    assert data["Sheet2"][-1]["age"] == "18"


def test_df_to_csv(tmp_path):

    df = DataFrame(np.random.randint(100, 1000, (10, 10)), columns=list("abcdefghij"))

    path = str(tmp_path / "df_to_csv.csv")

    provider.df_to_csv(df, path)
    

def test_df_to_excel(tmp_path):

    df = DataFrame(np.random.randint(100, 1000, (10, 10)), columns=list("abcdefghij"))

    path = str(tmp_path / "df_to_excel.xlsx")

    provider.df_to_excel(df, path, "one")
    provider.df_to_excel(df, path, "two")


def test_df_to_excel_fit_column_width(tmp_path: Path):

    path = str(tmp_path / "df_to_excel_fit_column_width.xlsx")

    data = [
        {"name11111111111111111111111111": "hhb", "age": 18},
        {"name11111111111111111111111111": "huabo", "age": "10000000000000000000000"},
        {"name11111111111111111111111111": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa22222222222222222", "age": "aaaaaaaaaaaa"},
    ]

    df = DataFrame(data)
    provider.df_to_excel(df, path, "test")


def test_df_to_excel_overwrite(tmp_path: Path):

    path = str(tmp_path / "df_to_excel_overwrite.xlsx")

    df = DataFrame(np.random.randint(100, 1000, (10, 10)), columns=list("abcdefghij"))
    provider.df_to_excel(df, path, "overwrite")

    df = DataFrame(np.random.randint(100, 1000, (5, 10)), columns=list("abcdefghij"))
    provider.df_to_excel(df, path, "overwrite")

    df_new = provider.read_excel_to_df(path, "overwrite")
    assert df_new.shape == (5, 10)


def test_split_row_to_single_sheet(tmp_path: Path):

    sheet_name = "Sheet1"
    file_name = os.path.basename(testdata["path"]).split(".")[0]

    datas = provider.read_excel_to_dict(testdata["path"], sheet_name)

    for data in datas:
        output = str(tmp_path / "{}-{}.xlsx".format(file_name, data["name"]))

        df = provider.dict_to_df(data)
        provider.df_to_excel(df, output, sheet_name)


def test_df_append_excel():

    data = [{"name": "{{name}}", "age": "{{data.int(18, 30)}}", "gender": "male", "height": 180}]

    df = DataFrame(data)

    provider.df_append_excel(df, testdata["path"], "Sheet1")


def test_append_excel(tmp_path: Path):

    path = str(tmp_path / "append.xlsx")

    data = {"name": "hhb", "age": 18, "height": 180}
    df = provider.dict_to_df(data)

    provider.df_to_excel(df, path, "append")
    provider.df_append_excel(df, path, "append")

    df_new = provider.read_excel_to_df(path, "append")

    assert df_new.shape == (2, 3)
    assert df_new["name"][0] == "hhb"
    assert df_new["name"][1] == "hhb"


def test_replace_macro_output_xlsx_override(tmp_path: Path):

    target = str(tmp_path / "replace_macro_override.xlsx")

    macro = [("{{name}}", "hhb")]
    provider.replace_macro_output(testdata["path"], macro, target=target, sheet="Sheet1")


def test_replace_macro_output_xlsx_append(tmp_path: Path):

    target = str(tmp_path / "replace_macro_override.xlsx")

    macro = [("{{name}}", "hhb")]
    provider.replace_macro_output(testdata["path"], macro, target=target, sheet="Sheet1", mode="a")


def test_replace_macro_output_csv(tmp_path: Path):

    target = str(tmp_path / "replace_macro_output.csv")

    macro = [("{{name}}", "hhb")]
    provider.replace_macro_output(testdata["path"], macro, target=target, sheet="Sheet1")

def test_str_to_bool():

    assert provider.str_to_bool("true") == True
    assert provider.str_to_bool("True") == True
    assert provider.str_to_bool("y") == True
    assert provider.str_to_bool("Y") == True
    assert provider.str_to_bool("yes") == True
    assert provider.str_to_bool("YES") == True
    assert provider.str_to_bool("1") == True

    assert provider.str_to_bool("false") == False
    assert provider.str_to_bool("False") == False
    assert provider.str_to_bool("n") == False
    assert provider.str_to_bool("N") == False
    assert provider.str_to_bool("no") == False
    assert provider.str_to_bool("NO") == False
    assert provider.str_to_bool("0") == False


def test_unpack_dict():

    nest_dict = {"a": 1, "b": {"c": 2, "d": 3, "e": {"f": 4}}, "g": {"h": 5}, "i": 6, "j": {"k": {"l": {"m": 8}}}}
    unpack_dict = provider.unpack_dict(nest_dict)

    assert unpack_dict == {"a": 1, "c": 2, "d": 3, "f": 4, "h": 5, "i": 6, "m": 8}


def test_replace_macro_replace():

    macro = [("{{user.id}}", "123456"), ("{{test.id}}", "12321")]

    listdata = ["abc {{user.id}} ssss", "abc {{test.id}} ssss", "abc {{encry.md5('123')}} ssss"]
    dictdata = {"inline": "abc {{unknown}} ssss", "prefix": "abc {{user.id}}", "suffix": "{{user.id}} abc d"}

    args, kw = provider.replace_macro(macro, *listdata, **dictdata)

    assert args == ("abc 123456 ssss", "abc 12321 ssss", "abc 202cb962ac59075b964b07152d234b70 ssss")
    assert kw == {"inline": "abc {{unknown}} ssss", "prefix": "abc 123456", "suffix": "123456 abc d"}

def test_replace_macro_different_module_methods():

    macro = [("{{user.id}}", "123456"), ("{{test.id}}", "12321")]

    listdata = [
        "abc {{user.id}} ssss",
        "abc {{test.id}} ssss"
    ]

    args, kw = provider.replace_macro(macro, *listdata)

    logging.info(args)
    logging.info(kw)


def test_replace_macro_args_are_none():

    macro = [("{{user.id}}", "123456"), ("{{test.id}}", "12321")]

    kw = {"id": "{{user.id}}"}

    args, kw = provider.replace_macro(macro)

    logging.info(args)
    logging.info(kw)

    assert args == ()
    assert kw == {}


def test_replace_macro_muti_macro():

    macro = [("{{user.id}}", "123456"), ("{{test.id}}", "12321")]

    args = ["{{user.id}}", "{{test.id}}"]
    kw = {"id": "{{user.id}}, {{test.id}}"}

    args, kw = provider.replace_macro(macro, *args, **kw)

    logging.info(args)
    logging.info(kw)

    assert args == ("123456", "12321")
    assert kw == {"id": "123456, 12321"}


def test_replace_macro_nested_macro():

    kw = {
        "imei": "{{encry.md5(data.imei())}}",
        "imei_upper": "{{encry.md5('865790026966479'.upper())}}",
        "oaid": "{{encry.md5(data.oaid())}}",
        "androidid": "{{encry.md5(data.androidid())}}",
        "idfa": "{{encry.md5(data.idfa())}}",
        "mac": "{{encry.md5(data.mac())}}",
        "openudid": "{{encry.md5(data.openudid())}}",
    }

    args, kw = provider.replace_macro(None, None, **kw)

    logging.info(args)
    logging.info(kw)
