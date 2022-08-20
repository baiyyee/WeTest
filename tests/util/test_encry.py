import logging
import requests
from pathlib import Path
from WeTest.util import encry


def test_aes():

    logging.info(encry.aes_encrypt("hhb@!@#$%^&*"))
    logging.info(encry.aes_encrypt("hhb@!@#$%^&*", "0123456789abcdef"))

    # Note: AES encry result is different every time
    assert encry.aes_encrypt("hhb@!@#$%^&*") != encry.aes_encrypt("hhb@!@#$%^&*", "0123456789abcdef")
    assert encry.aes_decrypt("1abd3ec4c45552d5953ed154", "812b03eece97de61b5697f7b1c908a18", "0123456789abcdef") == "hhb@!@#$%^&*"


def test_md5(tmp_path: Path):

    assert encry.md5("") == "d41d8cd98f00b204e9800998ecf8427e"
    assert encry.md5("abc") == "900150983cd24fb0d6963f7d28e17f72"
    assert encry.md5("中文") == "a7bac2239fcdcb3a067903d8077c4a07"

    path = tmp_path / "test.txt"
    path.write_text("test")
    assert encry.md5(str(path), "file") == "098f6bcd4621d373cade4e832627b4f6"


def test_mma_md5():

    assert encry.mma_md5("") == "d41d8cd98f00b204e9800998ecf8427e".upper()
    assert encry.mma_md5("abc") == encry.md5("abc".upper()).upper()
    assert encry.mma_md5("中文") == "a7bac2239fcdcb3a067903d8077c4a07".upper()
    assert encry.mma_md5("a7bac2239fcdcb3a067903d8077c4a07") == "a7bac2239fcdcb3a067903d8077c4a07".upper()


def test_ismd5string():

    assert encry.is_md5_string("abc") == False
    assert encry.is_md5_string(encry.md5("abc")) == True
    assert encry.is_md5_string(encry.md5("abc").upper()) == True
    assert encry.is_md5_string("G" * 32) == False
    assert encry.is_md5_string("A" * 32) == True
    assert encry.is_md5_string("A" * 33) == False


def test_ishexstring():

    assert encry.is_hex_string("0123456789abcdef") == True
    assert encry.is_hex_string("h") == False
    assert encry.is_hex_string("中文") == False


def test_sha1():

    assert encry.sha1("") == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    assert encry.sha1("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d"
    assert encry.sha1("中文") == "7be2d2d20c106eee0836c9bc2b939890a78e8fb3"


def test_url_encode():

    assert encry.url_encode({"education": "高中"}) == "education=%E9%AB%98%E4%B8%AD"
    assert encry.url_encode("高中") == "%E9%AB%98%E4%B8%AD"
    assert encry.url_encode("http://www.baidu.com") == "http%3A%2F%2Fwww.baidu.com"
    assert encry.url_encode('~!@#$%^&*()_+{}|:"<>?') == "~%21%40%23%24%25%5E%26%2A%28%29_%2B%7B%7D%7C%3A%22%3C%3E%3F"


def test_urldecode():

    assert encry.url_decode("education=%E9%AB%98%E4%B8%AD") == "education=高中"
    assert encry.url_decode("%E9%AB%98%E4%B8%AD") == "高中"


def test_base64_encode(tmp_path: Path):

    # Base64 encode string
    logging.info(encry.base64_encode("http://a.b.c.d"))
    logging.info(encry.base64_encode("https://www.baidu.com/s?a=1&b=2#c"))
    logging.info(encry.base64_decode("5YWz6ZSu6K-N"))
    logging.info(encry.base64_decode("5YWz6ZSu6K-N", type="string"))
    logging.info(encry.base64_encode("年龄19"))
    logging.info(encry.base64_encode("关键词03"))

    assert encry.base64_encode("keyword") == "a2V5d29yZA=="
    assert encry.base64_decode("5YWz6ZSu6K-N") == "关键词"

    # Base64 encode image
    image = requests.get("https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png").content
    path = tmp_path / "test.jpg"
    path.write_bytes(image)
    logging.info(encry.base64_decode(str(path), type="image"))


def test_base64_decode():

    logging.info(encry.base64_encode("http://10.77.0.1/show.html?a="))
    assert encry.base64_decode("a2V5d29yZA==") == "keyword"
    assert encry.base64_decode("5YWz6ZSu6K-N") == "关键词"
