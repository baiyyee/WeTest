import io
import pytest
import pandas
import logging
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from WeTest.util import compare, path
from pandas.util.testing import assert_frame_equal


source_data = """
price,id,name,date
5.1,10,George Maharis,2019/12/2
4.9,11,Michael Bluth,2019/12/3
5.4,12,George Bluth,2019/12/4
6.8,13,Bob Loblow,2019/12/5
6.7,14,Lucille Bluth,2019/12/6
"""

target_01_data = """
id,price,name,date,age
10,5.1,George Maharis,2019/12/2,11
11,4.9,Michael Bluth,2019/12/3,16
12,5.4,George Bluth,2019/12/4,14
13,6.8,Bob Loblow,2019/12/5,11
14,67.0,Lucille Bluth,2019/12/6,13
15,6,Loose Seal Bluth,2019/12/6,12
"""

target_02_data = """
id,price,name,date
14,6.7,Lucille Bluth,2019/12/6
10,5.1,George Maharis,2019/12/2
11,4.9,Michael Bluth,2019/12/3
12,5.4,George Bluth,2019/12/4
13,6.8,Bob Loblow,2019/12/5
"""

source = pandas.read_csv(io.StringIO(source_data))
target_01 = pandas.read_csv(io.StringIO(target_01_data))
target_02 = pandas.read_csv(io.StringIO(target_02_data))


def test_campare_df():

    result = compare.campare_df(source=source, target=target_01, join_columns="id")

    assert result == False


@pytest.mark.xfail(reason="Diffrent data, will always be fail")
def test_assert_frame_equal():

    assert_frame_equal(source, target_01)


def test_campare_df_thesamedata():

    result = compare.campare_df(source=source, target=source, join_columns="id")

    assert result == True


def test_campare_df_samedatawithdifferentorder():

    result = compare.campare_df(source=source, target=target_02, join_columns="id")

    assert result == True


def test_campare_dict():

    dict_01 = {"a": 1, "b": 2, "c": 3}
    dict_02 = {"a": 2, "d": 4, "c": 3}
    dict_03 = {"a": 2, "d": 4, "c": 3}

    result1 = compare.campare_dict(dict_01, dict_02)
    result2 = compare.campare_dict(dict_02, dict_03)
    logging.info(result1)
    logging.info(result2)

    assert result1 == [("change", "a", (1, 2)), ("add", "", [("d", 4)]), ("remove", "", [("b", 2)])]
    assert result2 == []


def test_campare_list():

    list_01 = [1, 2, 3]
    list_02 = [3, 2, 1]

    assert compare.campare_list(list_01, list_02)


def test_campare_file():

    file1 = "test/util/test_campare.py"
    file2 = "test/util/test_client.py"

    assert compare.campare_file(file1, file1) == True
    assert compare.campare_file(file1, file2) == False


def test_campare_image_str(tmp_path):
    image = requests.get("https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png").content

    img_ori = tmp_path / "test.png"
    img_new = path.replace_name(str(img_ori), "img_new")

    path.write_bytes(image, img_ori)

    img = Image.open(img_ori)
    draw = ImageDraw.Draw(img)
    draw.text((28, 26), "Baidu", fill=(0, 0, 0))
    img.save(img_new)

    assert compare.campre_image(str(img_ori), img_new, output=f"{tmp_path / 'test_campare_image_str.png'}") == False


def test_campare_image_bytes(tmp_path):
    image = requests.get("https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png").content
    image = BytesIO(image)

    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    draw.text((28, 26), "Baidu", fill=(0, 0, 0))
    image_new = BytesIO()
    img.save(image_new, "png")

    output = str(tmp_path / "test_campare_image_bytes.png")

    assert compare.campre_image(image, image_new, output=output) == False


def test_campare_schema():

    json = {"data": [1, 2, 3]}
    schema = {"type": "object", "required": ["data"], "properties": {"data": {"type": "array", "items": {"type": "number"}}}}

    assert compare.campare_schema(json, schema)
