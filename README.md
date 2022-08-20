# WeTest

**WeTest** is a simple, yet useful, test toolkit.

WeTest allows you to do automation test project extremely easily, like api test, macro support, tracker requests, testdata build, common clients connection...

Just try a little test scenario:


- **testdata**: testdata.xlsx

| tc_id        | tc_desc    | method | headers                                                        | json | data | protocol | domain     | path     | ip               | accessKey   | plain_string | loop | expect_code | expect_response |
| ------------ | ---------- | ------ | -------------------------------------------------------------- | ---- | ---- | -------- | ---------- | -------- | ---------------- | ----------- | ------------ | ---- | ----------- | --------------- |
| ip_parse_001 | ipv4_parse | get    | user-agent > {{data.user_agent()}} \| referer > {{data.url()}} |      |      | https    | {{domain}} | {{path}} | {{ipv4.beijing}} | alibaba-inc |              |      | 200         | "city":"北京"   |

- **testcase**: tests/tool/test_tracker.py

```python
import pytest
from WeTest.tool import tracker
from WeTest.util import provider


data = provider.read_excel_to_dict("testdata.xlsx", 0)

@pytest.mark.parametrize("data", data, ids=lambda data: "{}-{}".format(data["tc_id"], data["tc_desc"]))
def test_ipparse_ipv4(data):

    macro = [("{{domain}}", "ip.taobao.com"), ("{{path}}", "outGetIpInfo"), ("{{ipv4.beijing}}", "1.2.5.0")]

    tracker.send(macro, None, **data)

```

```console
$ pytest pytest tests/tool/test_tracker.py::test_ipparse_ipv4

collecting ... 
-------------------------------------------------------------------------------------- live log call --------------------------------------------------------------------------------------
2022-08-20 15:38:17 [INFO] 
========================================= [ REQUEST ] =========================================
GET https://ip.taobao.com/outGetIpInfo?request_id=jp_parase_001_ipv4_parse_0001&ip=1.2.5.0&accessKey=alibaba-inc
user-agent: Mozilla/5.0 (Linux; Android 5.0) AppleWebKit/536.2 (KHTML, like Gecko) Chrome/63.0.850.0 Safari/536.2
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
referer: http://www.fanding.cn/

None

========================================= [ RESPONSE ] =========================================
200  https://ip.taobao.com/outGetIpInfo?request_id=jp_parase_001_ipv4_parse_0001&ip=1.2.5.0&accessKey=alibaba-inc
Date: Sat, 20 Aug 2022 07:38:12 GMT
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
Set-Cookie: XSRF-TOKEN=8b64ecea-e4db-41fe-8351-98f87e45b732; Path=/
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Content-Encoding: gzip
Server: Tengine/Aserver
EagleEye-TraceId: 213fc9b716609810926637035e8a94
Strict-Transport-Security: max-age=31536000
Timing-Allow-Origin: *

{"data":{"area":"","country":"中国","isp_id":"100017","queryIp":"1.2.5.0","city":"北京","ip":"1.2.5.0","isp":"电信","county":"","region_id":"110000","area_id":"","county_id":null,"region":"北京","country_id":"CN","city_id":"110100"},"msg":"query success","code":0}


 tests/tool/test_tracker.py::test_ipparse_ipv4[jp_parase_001-ipv4_parse] ✓                                                                                                  100% ██████████

Results (1.16s):
       1 passed
```

## Installing WeTest and Supported Versions

WeTest is available on PyPI:

- For common use:

```console
$ python -m pip install WeTest
```

- For **Jira/RabbitMQ/AWS S3/SSH/SFTP** support:
```console
$ python -m pip install WeTest[client]
```

- For **Hive** support:
```console
$ python -m pip install WeTest[hive]
```

## Features

WeTest is ready for the demands of building automation test project, for the needs of today.

- util
  - algorithm
    - upstream_round_robin
  - api
    - request
    - upload
    - download
  - client
    - database
    - rabbitmq
    - sftp
    - ssh
    - nacos
    - s3
    - hive
  - compare
    - dataframe
    - dict
    - list
    - schema
  - config
    - yaml
    - ini
    - json
  - date
    - format
    - convert
    - datetime
    - timestamp
  - encry
    - aes
    - md5
    - url
    - sha1
    - base64
  - network
    - ip
    - url
    - useragent
  - notication
    - work wechat
    - wechat(todo)
    - email(todo)
  - provider
    - dataframe & excel
    - read & output
    - unpack dict
    - str to bool
    - replace macro
  - request
    - request by remote ip (in LB)
    - get romote ip
    - get redirect history
    - async request
    - bulk request
    - upload
    - download
    - log response
  - testdata
    - fake data


- tool
  - cookdata
    - cook df data
    - cook db data
  - decorator
    - timeit
  - logtime
    - timestamp
  - jira issue analytics
  - server(todo)
    - online api call
    - data visualization
  - tracker



Install WeTest, Enjoy your test!