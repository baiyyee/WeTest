import pytest
import logging
import asyncio
from pathlib import Path
from aiohttp import ClientSession
from WeTest.util import date, request


def test_get_remote_ip():

    url = "http://www.baidu.com"
    ip = request.get_remote_ip(url)

    logging.info(ip)


def test_request_by_ip():

    url = "https://www.bing.com"
    ip = request.get_remote_ip(url)
    request.request_by_ip(url, ip)


def test_get_redirect_history():

    expect = [(302, "http://www.baidu.com/"), (200, "https://www.baidu.com/")]

    url = "http://www.baidu.com"
    actual = request.get_redirect_history(url)

    assert actual == expect


def test_request_get():

    response = request.request("get", url="http://www.baidu.com")
    status_code = response.status_code

    response = request.request("get", url="http://www.baidu.com", params={"a": 1, "b": 2})
    url = response.url

    assert status_code == 200
    assert url == "https://www.baidu.com/?a=1&b=2"


def test_request_post():

    response = request.request("post", url="http://www.baidu.com")
    assert response.status_code == 200

    response = request.request("post", url="http://www.baidu.com", data={"a": 1, "b": 2})
    assert response.status_code == 200

    response = request.request("post", url="http://www.baidu.com", json={"a": 1, "b": 2})
    assert response.status_code == 200

    response = request.request("post", url="http://www.baidu.com", data={"a": 1, "b": 2}, json={"a": 1, "b": 2})
    assert response.status_code == 200

    response = request.request(
        "post", url="http://www.baidu.com", params={"a": 1, "b": 2}, data={"a": 1, "b": 2}, json={"a": 1, "b": 2}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_request_get(session: ClientSession):

    response = await request.async_request(session=session, url="http://www.baidu.com", method="get")
    assert response.status == 200

    response = await request.async_request(session=session, url="http://www.baidu.com", method="get", params={"a": 1, "b": 2})
    assert str(response.url) == "http://www.baidu.com/?a=1&b=2"

    response = await request.async_request(session=session, url="http://www.baidu.com", method="get", params={"a": 1, "b": None})
    assert str(response.url) == "http://www.baidu.com/?a=1"


@pytest.mark.asyncio
async def test_async_request_post(session: ClientSession):

    response = await request.async_request(session=session, url="http://www.baidu.com", method="post")
    assert response.status == 200

    response = await request.async_request(session=session, url="http://www.baidu.com", method="post", data={"a": 1, "b": 2})
    assert response.status == 200

    response = await request.async_request(session=session, url="http://www.baidu.com", method="post", json={"a": 1, "b": 2})
    assert response.status == 200

    response = await request.async_request(
        session=session, url="http://www.baidu.com", method="post", params={"a": 1, "b": 2}, json={"a": 1, "b": 2}
    )
    assert response.status == 200

    response = await request.async_request(
        session=session, url="http://www.baidu.com", method="post", params={"a": 1, "b": None}, data={"a": 1, "b": None}
    )
    assert response.status == 200


def test_bulk_request():

    urls = ["http://www.baidu.com"] * 10
    task = request.bulk_request("get", urls)
    asyncio.run(task)


def test_upload_download(tmp_path: Path):

    # download
    url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    path = request.download(url, str(tmp_path))

    # upload
    url = "https://graph.baidu.com/upload?uptime={}".format(date.get_unixtime(13))
    response = request.upload(url, path)
    assert response.status_code == 200
