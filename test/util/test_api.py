from pathlib import Path
from WeTest.util import date
from WeTest.util.api import API


path = "/"


def test_api_get(api: API):

    response = api.request("get", path)
    status_code = response.status_code

    response = api.request("get", path, params={"a": 1, "b": 2})
    url = response.url

    assert status_code == 200
    assert url == "https://www.baidu.com/?a=1&b=2"


def test_api_post(api: API):

    response = api.request("post", path)
    assert response.status_code == 200

    response = api.request("post", path, data={"a": 1, "b": 2})
    assert response.status_code == 200

    response = api.request("post", path, json={"a": 1, "b": 2})
    assert response.status_code == 200

    response = api.request("post", path, data={"a": 1, "b": 2}, json={"a": 1, "b": 2})
    assert response.status_code == 200

    response = api.request("post", path, params={"a": 1, "b": 2}, data={"a": 1, "b": 2}, json={"a": 1, "b": 2})
    assert response.status_code == 200


def test_api_upload_download(api: API, tmp_path: Path, monkeypatch):

    # download
    path = "/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    path = api.download(path, str(tmp_path))

    # upload
    url = "/upload?uptime={}".format(date.get_unixtime(13))

    # temporary changed the domain and recoverd once its finished
    monkeypatch.setattr(api, "domain", "https://graph.baidu.com")

    response = api.upload(url, [path])
    assert response.status_code == 200


def test_get_api_domain(api: API):

    # verify the domain recoverd as before
    assert api.domain == "https://www.baidu.com"
