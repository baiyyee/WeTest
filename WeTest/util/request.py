import os
import pypeln
import logging
import textwrap
import requests
from WeTest import const
from WeTest.util import encry
from aiohttp import ClientSession
from requests import Response, Session
from urllib.parse import urlparse, urlunparse
from aiohttp.client import _RequestContextManager


def request_by_ip(url: str, ip: str):
    """Request to specific host by ip"""

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    headers = {"Connection": "close", "Host": host}

    # Replaced domin with ip and add host to headers, then we can request to the specific host
    url = urlunparse((parsed_url.scheme, ip, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    response = request("get", url, headers=headers, allow_redirects=False, stream=False, verify=False)

    code = response.status_code

    if str(code)[0] == "3":
        location = response.headers["Location"]
    else:
        location = None

    logging.info("{}, {}".format(code, url))

    # regression
    if location != None and urlparse(location).netloc != host:
        historys = get_redirect_history(location)
        for code, url in historys:
            logging.info("{}, {}".format(code, url))
    else:
        if str(code)[0] == "3" and urlparse(location).netloc == host:
            request_by_ip(location, ip)


def get_remote_ip(url: str) -> str:

    response = requests.get(url, stream=True)
    remote_ip = response.raw._original_response.fp.raw._sock.getpeername()[0]

    return remote_ip


def get_redirect_history(url: str) -> list:

    response = request("get", url)

    historys = []
    for history in response.history:
        historys.append((history.status_code, history.url))

    historys.append((response.status_code, response.url))

    return historys


def request(method: str, url: str, session: Session = Session(), **kwargs) -> Response:

    response = None

    valid_key = [
        "method",
        "url",
        "params",
        "data",
        "headers",
        "cookies",
        "files",
        "auth",
        "timeout",
        "allow_redirects",
        "proxies",
        "hooks",
        "stream",
        "verify",
        "cert",
        "json",
    ]

    kwargs = {k: v for k, v in kwargs.items() if k in valid_key and v is not None}

    # Replace the default UA
    kwargs.setdefault("headers", {"User-Agent": const.USER_AGENT})

    try:
        response = session.request(method=method, url=url, **kwargs)

        logging.info(log(response))

    except Exception as e:
        logging.error("========================================= [ EXCEPTION ] =========================================")
        logging.error(e)

    return response


def async_request(session: ClientSession, method: str, url: str, **kwargs) -> _RequestContextManager:

    valid_key = [
        "method",
        "str_or_url",
        "params",
        "data",
        "json",
        "cookies",
        "headers",
        "skip_auto_headers",
        "auth",
        "allow_redirects",
        "max_redirects",
        "compress",
        "chunked",
        "expect100",
        "raise_for_status",
        "read_until_eof",
        "proxy",
        "proxy_auth",
        "timeout",
        "verify_ssl",
        "fingerprint",
        "ssl_context",
        "ssl",
        "proxy_headers",
        "trace_request_ctx",
    ]

    kwargs = {k: v for k, v in kwargs.items() if k in valid_key}

    try:
        if ("params" in kwargs) and kwargs["params"]:
            params = {key: value for key, value in kwargs["params"].items() if value is not None}
            kwargs.update(params=params)

        return session._request(method, url, **kwargs)

    except Exception as e:
        logging.error("========================================= [ EXCEPTION ] =========================================")
        logging.error(e)


async def bulk_request(method: str, urls: list, workers: int = 100, **kwargs):
    async def request(session: ClientSession, url: str):
        async with session.request(method, url, **kwargs) as response:
            logging.info("{}, {}".format(response.status, url))
            return await response.read()

    async def task():
        async with ClientSession() as session:
            await pypeln.task.each(lambda url: request(session, url), urls, workers=workers, run=False)

    return await task()


def upload(url: str, path: str, session: Session = Session(), **kwargs) -> Response:

    kwargs.setdefault("files", {"file": open(path, "rb")})

    return request("post", url, session, **kwargs)


def download(url: str, path: str, session: Session = Session(), chunk_size: int = 128) -> str:

    response = request("get", url, session, stream=True)

    if "Content-Disposition" in response.headers:
        filename = response.headers["Content-Disposition"].split(";")[-1].strip().split("=")[-1]
    else:
        filename = str(response.url).split("/")[-1].split("?")[0]

    path = encry.url_decode(os.path.join(path, filename)).replace(":", "_")

    with open(path, "wb") as f:
        for content in response.iter_content(chunk_size=chunk_size):
            f.write(content)

        logging.info(f"Download file to: {path}")

    return path


def log(response: Response) -> str:

    format_headers = lambda data: "\n".join(f"{k}: {v}" for k, v in data.items())

    return textwrap.dedent(
        """
        ========================================= [ REQUEST ] =========================================
        {request.method} {request.url}
        {request_headers}

        {request.body}

        ========================================= [ RESPONSE ] =========================================
        {response.status_code} {response.reason} {response.url}
        {response_headers}

        {response.text}
    """
    ).format(
        request=response.request,
        response=response,
        request_headers=format_headers(response.request.headers),
        response_headers=format_headers(response.headers),
    )
