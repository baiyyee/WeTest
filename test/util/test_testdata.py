import logging
from pathlib import Path
from WeTest.util import testdata


def test_userinfo():

    logging.info("Random Gender:   {}".format(testdata.gender()))
    logging.info("Random Name:   {}".format(testdata.name()))
    logging.info("Random Password:   {}".format(testdata.password()))
    logging.info("Random Phone:   {}".format(testdata.phone()))
    logging.info("Random Address:    {}".format(testdata.address()))
    logging.info("Random Postcode:    {}".format(testdata.postcode()))
    logging.info("Random Email:   {}".format(testdata.email()))
    logging.info("Random Username: {}".format(testdata.username()))
    logging.info("Random UUID:  {}".format(testdata.uuid()))
    logging.info("Random City:    {}".format(testdata.city()))
    logging.info("Random Province:    {}".format(testdata.province()))
    logging.info("Random Country:    {}".format(testdata.country()))


def test_deviced_id():

    logging.info("Random COOKIE:   {}".format(testdata.random_cookie("https://www.baidu.com")))
    logging.info("Random IDFA:     {}".format(testdata.idfa()))
    logging.info("Random IMEI:     {}".format(testdata.imei()))
    logging.info("Random OAID:     {}".format(testdata.oaid()))
    logging.info("Random MAC:      {}".format(testdata.mac()))
    logging.info("Random AAID:     {}".format(testdata.aaid()))
    logging.info("Random ANDROIDID:{}".format(testdata.androidid()))
    logging.info("Random OPENUDID: {}".format(testdata.openudid()))


def test_datetime():

    logging.info("Random Date2:   {}".format(testdata.datetime("%Y/%m/%d")))
    logging.info("Random Time1:  {}".format(testdata.time()))
    logging.info("Random Time2:  {}".format(testdata.time("%H_%M_%S")))


def test_internet():

    logging.info("Random Protocol:   {}".format(testdata.protocol()))
    logging.info("Random Domain:   {}".format(testdata.domain()))
    logging.info("Random URI:    {}".format(testdata.uri()))
    logging.info("Random URL:    {}".format(testdata.url()))


def test_ip():

    logging.info("Random IPV4:   {}".format(testdata.ipv4()))
    logging.info("Random IPV6:   {}".format(testdata.ipv6()))
    logging.info("Random IPV4 - Wuhan:   {}".format(testdata.ipv4("武汉")))
    # logging.info("Random IPV6 - Wuhan:   {}".format(testdata.ipv6("武汉")))


def test_encrypt():

    logging.info("Random MD5:    {}".format(testdata.md5()))
    logging.info("Random SHA1:   {}".format(testdata.sha1()))
    logging.info("Random SHA256: {}".format(testdata.sha256()))


def test_testdatadata():

    logging.info("Random Boolen: {}".format(testdata.boolean()))
    logging.info("Random Int:   {}".format(testdata.int(100, 999)))

    logging.info("Random Value:     {}".format(testdata.random_choice(["A", "B", "C", "D"])))
    logging.info("Random Value:     {}".format(testdata.random_choice(["A", "B", "C", "D"], n=2)))
    logging.info("Random Value:     {}".format(testdata.random_choice([0, 1])))
    logging.info("Random String1:{}".format(testdata.string()))
    logging.info("Random String2:{}".format(testdata.string(length=10)))
    logging.info("Random String3:{}".format(testdata.string(seeds="1234567890", length=10)))
    logging.info("Random String4:{}".format(testdata.string(min=1, max=100)))
    logging.info("Random String5:{}".format(testdata.string(seeds="1234567890abcdef")))
    logging.info("Random String6:{}".format(testdata.string(seeds="1234567890abcdef", min=1, max=32)))
    logging.info("Random Chinese String: {}".format(testdata.chinese_chars()))
    logging.info("Random ASCII String: {}".format(testdata.ascii_letters()))
    logging.info("Random ASCII String2: {}".format(testdata.ascii_letters(min=1, max=20)))
    logging.info("Random Chinese String2: {}".format(testdata.chinese_chars(1, 20)))
    logging.info("Random Sentence:   {}".format(testdata.sentence()))
    logging.info("Random Text:   {}".format(testdata.text()))
    logging.info("Random Word:   {}".format(testdata.word()))
    logging.info("Random Number:   {}".format(testdata.digits()))
    logging.info("Random Number2:   {}".format(testdata.digits(min=1, max=10)))

    logging.info("Special English Chars 1:  {}".format(testdata.specialchars_english()))
    logging.info("Special English Chars 2:  {}".format(testdata.specialchars_english(seeds="~!@#$%^&*()_+|}{:<>?")))
    logging.info("Special English Chars 3:  {}".format(testdata.specialchars_english("~!@#$%^&*()_+|}{:<>?")))

    logging.info("Special Chinese Chars1:  {}".format(testdata.specialchars_chinese()))
    logging.info("Special Chinese Chars2:  {}".format(testdata.specialchars_chinese(seeds="·！@#￥%……&*【】、；’，。")))
    logging.info("Special Chinese Chars3:  {}".format(testdata.specialchars_chinese("·！@#￥%……&*【】、；’，。")))


def test_fakeuseragent():

    logging.info("Random Chrome UA : " + testdata.user_agent("chrome"))
    logging.info("Random Firefox UA: " + testdata.user_agent("firefox"))
    logging.info("Random IE UA     : " + testdata.user_agent("ie"))
    logging.info("Random Safari UA : " + testdata.user_agent("safari"))
    logging.info("Random Opera UA  : " + testdata.user_agent("opera"))
    logging.info("Random Android UA: " + testdata.user_agent("android"))
    logging.info("Random iOS UA    : " + testdata.user_agent("ios"))
    logging.info("Random Windows UA: " + testdata.user_agent("win"))
    logging.info("Random Linux UA  : " + testdata.user_agent("linux"))
    logging.info("Random MAC UA    : " + testdata.user_agent("mac"))
    logging.info("Random UA        : " + testdata.user_agent())


def test_date_between():

    logging.info("Get Date Between Range: " + testdata.date_between("20210612", "20210613"))
    logging.info("Get Date Between Range: " + testdata.date_between("2021/06/12", "2021/06/13"))
    logging.info("Get Date Between Range: " + testdata.date_between("2021-06-12", "2021-06-13"))
    logging.info("Get Date Between Range: " + testdata.date_between("20210612", "2021-06-13"))
    logging.info("Get Date Between Range: " + testdata.date_between("20210612", "2021-06-13", "YYYY/MM/DD"))
    logging.info("Get Date Between Range: " + testdata.date_between("20210612", "2021-06-13", "YYYYMMDD"))


def test_timestamp_between():

    logging.info("Get Timestamp Between Range: " + str(testdata.timestamp_between("2020-07-28", "2020-07-28")))
    logging.info("Get Timestamp Between Range: " + str(testdata.timestamp_between("2020-07-28 00:00:00", "2020-07-28 23:59:59")))
    logging.info(
        "Get Timestamp Between Range: " + str(testdata.timestamp_between("2020-07-28 00:00:00.100", "2020-07-28 23:59:59.999"))
    )
    logging.info("Get Timestamp Between Range: " + str(testdata.timestamp_between("2020/07/28 00:00:00", "2020/07/28 23:59:59")))
    logging.info("Get Timestamp Between Range: " + str(testdata.timestamp_between("2020/07/28 00:00:00", "2020/07/28 00:00:02")))


def test_size(tmp_path: Path):

    path_1 = str(tmp_path / "1.txt")
    path_1b = str(tmp_path / "1b.txt")
    path_1kb = str(tmp_path / "1kb.txt")
    path_1mb = str(tmp_path / "1mb.txt")

    testdata.file_size("1", path_1)
    testdata.file_size("1b", path_1b)
    testdata.file_size("1kb", path_1kb)
    testdata.file_size("1mb", path_1mb)

    logging.info(f"Save file to: {tmp_path}")
