from WeTest.util import network


def test_get_domain():

    assert network.get_domain("http://www.baidu.com/index?name=hhb&age=18") == "www.baidu.com"


def test_parse_url():

    parsed_url = network.parse_url("http://www.baidu.com/index?name=hhb&age=18#index")

    assert parsed_url.scheme == "http"
    assert parsed_url.netloc == "www.baidu.com"
    assert parsed_url.path == "/index"
    assert parsed_url.query == "name=hhb&age=18"
    assert parsed_url.fragment == "index"


def test_get_ip():

    assert network.get_ip_by_range("127.0.0.0", "127.0.0.2") == ["127.0.0.0", "127.0.0.1", "127.0.0.2"]
    assert network.get_ip_by_range("2002:0118:d204:0:0:0:0:0", "2002:0118:d204:0:0:0:0:2") == [
        "2002:0118:d204:0000:0000:0000:0000:0000",
        "2002:0118:d204:0000:0000:0000:0000:0001",
        "2002:0118:d204:0000:0000:0000:0000:0002",
    ]


def test_parse_ip():

    expect_data_ipv4_mip = {
        "ip": "1.15.0.0",
        "isp": "方正宽带",
        "region": "北京",
        "country_id": "CN",
        "country": "中国",
        "city": "北京",
    }

    expect_data_ipv6 = {
        "ip": "2002:1b71:8000::",
        "isp": None,
        "region": None,
        "country_id": None,
        "country": None,
        "city": None,
    }

    assert network.parse_ip("1.15.0.0") == expect_data_ipv4_mip
    assert network.parse_ip("2002:1b71:8000::") == expect_data_ipv6


def test_parse_useragent():

    assert network.parse_useragent("") == {
        "is_mma": False,
        "user_agent": "",
        "browser_name": "Unknown",
        "browser_version": "Unknown",
        "system_name": "Unknown",
        "system_version": "Unknown",
        "platform": "MBL",
        "device": "PHN",
    }

    assert network.parse_useragent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    ) == {
        "is_mma": False,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "browser_name": "Chrome",
        "browser_version": "80.0.3987",
        "system_name": "Windows",
        "system_version": "Windows 10",
        "platform": "DSK",
        "device": "DSK",
    }

    assert network.parse_useragent("Unknown") == {
        "is_mma": False,
        "user_agent": "Unknown",
        "browser_name": "Unknown",
        "browser_version": "Unknown",
        "system_name": "Unknown",
        "system_version": "Unknown",
        "platform": "MBL",
        "device": "PHN",
    }

    assert network.parse_useragent("X11; Linux i686") == {
        "is_mma": False,
        "user_agent": "X11; Linux i686",
        "browser_name": "Unknown",
        "browser_version": "Unknown",
        "system_name": "Linux",
        "system_version": "Linux",
        "platform": "DSK",
        "device": "DSK",
    }

    assert network.parse_useragent("Android 1.6") == {
        "is_mma": True,
        "user_agent": "Android 1.6",
        "browser_name": "Android",
        "browser_version": "1.6",
        "system_name": "Android",
        "system_version": "Android 1.6",
        "platform": "MBL",
        "device": "PHN",
    }
