import logging
from requests import Session, Response
from .request import request, upload, download


class API:
    def __init__(self):

        self.headers = {}
        self.session = Session()
        self.proxies = None
        self.domain = None

    def set_domain(self, domain: str):

        self.domain = domain[:-1] if domain.endswith("/") else domain

    def set_headers(self, headers: dict):

        self.headers.update(headers)
        self.session.headers.update(self.headers)

    def get_token(
        self, url: str, email: str, password: str, client_id: str, client_secret: str, grant_type: str, proxies: dict
    ) -> dict:

        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "username": email,
            "password": password,
        }

        if proxies["enable"]:
            proxies = "{type}://{server}:{port}".format(**proxies)
            self.session.proxies = {"http": proxies, "https": proxies}

        response = request("POST", url, self.session, data=data).json()

        access_token = response["access_token"]
        token_type = response["token_type"]

        token = {"Authorization": f"{token_type} {access_token}"}

        return token

    def request(self, method: str, url: str, **kwargs) -> Response:

        response = None

        url = (self.domain + url) if self.domain else url

        try:
            response = request(method, url, self.session, **kwargs)

        except Exception as e:
            logging.error("========================================= [ EXCEPTION ] =========================================")
            logging.error(e)

        return response

    def upload(self, url: str, path: str, **kwargs) -> Response:

        url = (self.domain + url) if self.domain else url

        return upload(url, path, self.session, **kwargs)

    def download(self, url: str, path: str, chunk_size: int = 128) -> str:

        url = (self.domain + url) if self.domain else url

        return download(url, path, self.session, chunk_size=chunk_size)
