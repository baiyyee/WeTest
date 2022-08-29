import pytest
from WeTest.tool import tracker
from WeTest.util import provider


macro = [("{{test}}", "test_tracker")]

args = [
    "test={{test}}",
    "p_phone={{data.phone()}}",
    "p_gender={{data.gender()}}",
    "cookie={{data.string(seeds='ABCDEFG', length=10)}}",
    "ts={{date.get_unixtime(length=10)}}",
]

kwargs = {
    "tc_id": 1,
    "tc_desc": "send_request",
    "method": "get",
    "protocol": "https",
    "domain": "www.baidu.com",
    "path": "",
    "plain_string": "测试",
    "loop": 2,
}


# data = provider.read_excel_to_dict("doc/template/tracker.xlsx", 0)

# @pytest.mark.parametrize("data", data, ids=lambda data: "{}-{}".format(data["tc_id"], data["tc_desc"]))
# def test_ipparse_ipv4(data):
    
#     macro = [("{{domain}}", "ip.taobao.com"), ("{{path}}", "outGetIpInfo"), ("{{ipv4.beijing}}", "1.2.5.0")]

#     tracker.send(macro, None, **data)

def test_send_aync_requests_no_sleep():

    tracker.send(macro, *args, **kwargs)


def test_send_aync_requests_sleep():

    tracker.send(macro, *args, sleep=2, **kwargs)

@pytest.mark.asyncio
async def test_send_async_requests(session):

    await tracker.async_send(session, macro, *args, **kwargs)
