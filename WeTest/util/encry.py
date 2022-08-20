import string
import hashlib
import base64
from urllib import parse
from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def aes_encrypt(plain: str, key: str = "0123456789abcdef") -> tuple:

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key.encode(), AES.MODE_CFB, iv)

    encrypt_string = cipher.encrypt(plain.encode())

    return b2a_hex(encrypt_string).decode(), b2a_hex(iv).decode()


def aes_decrypt(encry: str, iv: str, key: str = "0123456789abcdef") -> str:

    cipher = AES.new(key.encode(), AES.MODE_CFB, a2b_hex(iv.encode()))
    plain = cipher.decrypt(a2b_hex(encry.encode())).decode()

    return plain


def md5(data: str, type: str = "string") -> str:

    if data and type == "file":
        with open(data, "rb") as file:
            data = file.read()
            return hashlib.md5(data).hexdigest()
    else:
        return hashlib.md5(data.encode(encoding="utf-8")).hexdigest()


def mma_md5(data: str) -> str:

    return data.upper() if is_md5_string(data) else md5(data.replace(":", "").upper()).upper()


def is_md5_string(data: str) -> bool:

    if len(data) != 32:
        return False
    else:
        return all(char in string.hexdigits for char in list(data))


def is_sha1_string(data: str) -> bool:

    if len(data) != 40:
        return False
    else:
        return all(char in string.hexdigits for char in list(data))


def is_hex_string(data: str) -> bool:

    return all(char in string.hexdigits for char in list(data))


def sha1(data: str) -> str:

    return hashlib.sha1(data.encode(encoding="utf-8")).hexdigest()


def base64_encode(data: str) -> str:

    encode = base64.urlsafe_b64encode(bytes(data, encoding="utf-8"))
    return str(encode, encoding="utf-8")


def base64_decode(path_or_buffer: str, type: str = "string") -> str:
    """Base64 decode string or image"""

    if type == "string":
        decode = base64.urlsafe_b64decode(bytes(path_or_buffer, encoding="utf-8"))
        return str(decode, encoding="utf-8")

    elif type == "image":
        with open(path_or_buffer, "rb") as f:
            iamge_base64 = base64.b64encode(f.read())
            return iamge_base64.decode()


def url_encode(data: str) -> str:

    if isinstance(data, dict):
        return parse.urlencode(data)
    elif isinstance(data, str):
        return parse.quote(data, safe="")


def url_decode(data: str) -> str:

    return parse.unquote(data)
