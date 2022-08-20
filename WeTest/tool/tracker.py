import time
from aiohttp import ClientSession
from ..util import provider, request


def get_request_params(macro: list, *args, **kwargs) -> dict:
    """Get request params"""
    
    url = ""

    # Default
    kwargs["protocol"] = kwargs.get("protocol", "http") or "http"
    kwargs["method"] = kwargs.get("method", "get") or "get"
    kwargs["loop"] = kwargs.get("loop", "1") or "1"
    kwargs["expect_code"] = kwargs.get("expect_code", "200") or "200"
    
    args, kwargs = provider.replace_macro(macro, *args, **kwargs)

    # Need to exclude columns like tc_* or expect_*  or loop during join url params
    buildin_columns = ["method", "headers", "json", "data", "protocol", "domain", "path", "plain_string", "loop"]
    exclude_columns = buildin_columns + [key for key in kwargs if "tc_" in key.lower() or "expect_" in key.lower()]


    for value in args:
        if value:
            url += "&{}".format(value)
        
    if kwargs.get("plain_string"):
        url += "&{}".format(kwargs.get("plain_string"))

    if kwargs.get("path"):
        url = "{protocol}://{domain}/{path}?request_id={tc_id}_{tc_desc}_{count}".format(**kwargs, count="{count:0>4d}") + url
    else:
        url = "{protocol}://{domain}?request_id={tc_id}_{tc_desc}_{count}".format(**kwargs, count="{count:0>4d}") + url
      
    kwargs["headers"] = {
        header.strip().split(">")[0].lower().strip(): header.strip().split(">")[1].strip()
        for header in kwargs.get("headers").split("|")
        
    } if kwargs.get("headers") else None
    
    kwargs["json"] = {
        json.strip().split("=")[0].strip(): json.strip().split("=")[1].strip()
        for json in kwargs.get("json").split("|")
        
    } if kwargs.get("json") else None
    
    kwargs["data"] = {
        data.strip().split("=")[0].strip(): data.strip().split("=")[1].strip()
        for data in kwargs.get("data").split("|")
        
    } if kwargs.get("data") else None
    
    kwargs["params"] = {key: value for key, value in kwargs.items() if key not in exclude_columns} or None
    
    kwargs["url"] = url

    return kwargs


def send(macro: list, *args, sleep: int = 0, **kwargs):
    """Send sync requests"""

    kwargs = get_request_params(macro, *args, **kwargs)
    loop = int(kwargs["loop"])
    url = kwargs["url"]

    for i in range(1, loop + 1):

        # Note: verify=False in requests
        kwargs.update(url=url.format(count=i, verify=False))
        
        response = request.request(**kwargs)

        assert response.status_code == int(kwargs["expect_code"])

        if kwargs.get("expect_response"):
            assert kwargs["expect_response"] in response.text

        time.sleep(sleep)


async def async_send(session: ClientSession, macro: list, *args, **kwargs):
    """Send async requests"""

    kwargs = get_request_params(macro, *args, **kwargs)
    loop = int(kwargs["loop"])
    url = kwargs["url"]

    for i in range(1, loop + 1):
        
        # Note: ssl=False in aiohttp
        kwargs.update(url=url.format(count=i), ssl=False)
        response = await request.async_request(session=session, **kwargs)

        assert response.status == int(kwargs["expect_code"])