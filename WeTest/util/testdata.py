import re
import random
import string
import requests
import pkg_resources
from .. import const
from faker import Faker
from . import date, config, network
from faker.providers import BaseProvider


RANDOMSRING_DIGITS = string.digits
RANDOMSRING_ASCII_LETTERS = string.ascii_letters
RANDOMSRING_DEFAULT_SEEDS = string.ascii_letters + string.digits
RANDOMSRING_ENGLISH_SPECIALCHARS_SEEDS = const.ENGLISH_SPECIALCHARS_SEEDS
RANDOMSRING_CHINESE_SPECIALCHARS_SEEDS = const.CHINESE_SPECIALCHARS_SEEDS


# Custom Faker Provider
class Provider(BaseProvider):
    def gender(self) -> str:
        return random.choice(["男", "女"])

    def random_cookie(self, url: str) -> str:
        return requests.get(url).cookies

    def imei(self) -> str:
        return self.random_string(seeds="0123456789", length=random.choice([14, 17]))

    def oaid(self) -> str:
        return self.random_string(seeds=RANDOMSRING_DEFAULT_SEEDS, length=16)

    def aaid(self) -> str:
        return self.idfa().lower()

    def androidid(self) -> str:
        return self.random_string(seeds="0123456789abcdef", length=random.choice([15, 16]))

    def idfa(self) -> str:
        random_string = self.random_string(seeds="0123456789abcdef", length=32)
        return "{}-{}-{}-{}-{}".format(
            random_string[0:8], random_string[8:12], random_string[12:16], random_string[16:20], random_string[20:37]
        )

    def openudid(self, md5: str) -> str:
        return "{}{}".format(md5, self.random_string(seeds=RANDOMSRING_DEFAULT_SEEDS, length=8).lower())

    def protocol(self) -> str:
        return random.choice(["http", "https"])

    def specialchars(self, seeds: str) -> str:
        return seeds

    def random_string(self, seeds: str, **kw) -> str:
        random_string = ""

        if kw:
            if "length" in kw:
                random_string = "".join(random.choices(seeds, k=kw["length"]))
            elif "min" in kw and "max" in kw:
                length = random.randint(kw["min"], kw["max"])
                random_string = "".join(random.choices(seeds, k=length))
            else:
                length = random.randint(1, 200)
                random_string = "".join(random.choices(seeds, k=length))

        return random_string

    def chinese_chars(self, min: int, max: int):
        # Reference: https://blog.csdn.net/JohinieLi/article/details/81127358

        return "".join(
            [
                bytes.fromhex("{:x}{:x}".format(random.randint(0xB0, 0xF7), random.randint(0xA1, 0xFE))).decode("gb18030")
                for _ in range(0, random.randint(min, max))
            ]
        )

    def random_choice(self, seeds: list, n: int) -> list:
        return random.choices(seeds, k=n)

    def ip(self, ip_type: str, region: str):
        geo_path = pkg_resources.resource_filename("WeTest", "config/geo.yaml")
        geo_seeds = config.read_yaml(geo_path)

        ip_range = geo_seeds[ip_type].get(region, "武汉")
        ip = random.choice(network.get_ip_by_range(ip_range[0], ip_range[1]))

        return ip

    def file_size(self, size: str, output: str, char: str) -> str:
        """Build Specific Size Text File"""

        b = 1
        kb = b * 1024
        mb = kb * 1024
        gb = mb * 1024
        tb = gb * 1024

        num = 1
        unit = "b"

        if re.search(r"\d+(\.\d+)?", size):
            num = re.search(r"\d+(\.\d+)?", size).group()

        if re.search(r"b|kb|mb|gb|tb", size.lower()):
            unit = re.search(r"b|kb|mb|gb|tb", size.lower()).group()

        size = eval(num) * eval(unit) * char

        with open(output, "w") as f:
            f.write(size)

        return output


fake = Faker(locale="zh_CN")
fake.add_provider(Provider)


def int(min: int, max: int) -> int:
    return fake.random_int(min, max)


def string(seeds: str = RANDOMSRING_DEFAULT_SEEDS, **kw) -> str:
    return fake.random_string(seeds=seeds, **kw)


def random_choice(seeds: str, n: int = 1) -> list:
    return fake.random_choice(seeds, n)


def specialchars_english(seeds: str = RANDOMSRING_ENGLISH_SPECIALCHARS_SEEDS) -> str:
    return fake.specialchars(seeds)


def specialchars_chinese(seeds: str = RANDOMSRING_CHINESE_SPECIALCHARS_SEEDS) -> str:
    return fake.specialchars(seeds)


def chinese_chars(min: int = 1, max: int = 200) -> str:
    return fake.chinese_chars(min, max)


def ascii_letters(seeds: str = RANDOMSRING_ASCII_LETTERS, **kw) -> str:
    return fake.random_string(seeds=seeds, **kw)


def digits(seeds: str = RANDOMSRING_DIGITS, **kw) -> str:
    return fake.random_string(seeds=seeds, **kw)


def number(n: int) -> int:
    return fake.random_number(n)


def boolean() -> bool:
    return fake.boolean()


def name() -> str:
    return fake.name()


def job() -> str:
    return fake.job()


def gender() -> str:
    return fake.gender()


def username() -> str:
    return fake.user_name()


def password(
    length: int = 6,
    is_contains_specialchars: str = True,
    is_contains_digits: bool = True,
    is_contains_uppercase: bool = True,
    is_contains_lowercase: bool = True,
) -> str:
    return fake.password(length, is_contains_specialchars, is_contains_digits, is_contains_uppercase, is_contains_lowercase)


def address() -> str:
    return fake.address()


def postcode() -> str:
    return fake.postcode()


def email() -> str:
    return fake.email()


def url() -> str:
    return fake.url()


def protocol() -> str:
    return fake.protocol()


def uri() -> str:
    return fake.uri()


def domain() -> str:
    return fake.domain_name()


def random_cookie(url: str) -> str:
    return fake.random_cookie(url)


def imei() -> str:
    return fake.imei()


def oaid() -> str:
    return fake.oaid()


def aaid() -> str:
    return fake.aaid()


def androidid() -> str:
    return fake.androidid()


def mac() -> str:
    return fake.mac_address()


def idfa() -> str:
    return fake.idfa()


def openudid() -> str:
    return fake.openudid(fake.md5())


def ipv4(region: str = None) -> str:
    return fake.ip("ipv4", region) if region else fake.ipv4()


def ipv6(region: str = None) -> str:
    return fake.ip("ipv6", region) if region else fake.ipv6()


def phone() -> str:
    return fake.phone_number()


def text() -> str:
    return fake.text()


def word() -> str:
    return fake.word()


def sentence() -> str:
    return fake.sentence()


def city() -> str:
    return fake.city()


def province() -> str:
    return fake.province()


def country() -> str:
    return fake.country()


def md5() -> str:
    return fake.md5()


def sha1() -> str:
    return fake.sha1()


def sha256() -> str:
    return fake.sha256()


def uuid() -> str:
    return fake.uuid4()


def datetime(pattern: str = "%Y-%m-%d") -> str:
    return fake.date(pattern)


def time(pattern: str = "%H:%M:%S") -> str:
    return fake.time(pattern)


def date_between(start_date: str, end_date: str, fmt: str = "YYYY-MM-DD") -> str:
    return random.choice(date.get_day_by_range(start_date, end_date, fmt))


def timestamp_between(start_date, end_date, frame="second") -> str:
    return random.choice(date.get_timestamp_by_range(start_date, end_date, frame))


def user_agent(type: str = None) -> str:
    if not type:
        return fake.user_agent()
    if type.lower() == "chrome":
        return fake.chrome()
    elif type.lower() == "firefox":
        return fake.firefox()
    elif type.lower() == "ie":
        return fake.internet_explorer()
    elif type.lower() == "safari":
        return fake.safari()
    elif type.lower() == "opera":
        return fake.opera()
    elif type.lower() == "android":
        return fake.android_platform_token()
    elif type.lower() == "ios":
        return fake.ios_platform_token()
    elif type.lower() == "win":
        return fake.windows_platform_token()
    elif type.lower() == "linux":
        return fake.linux_platform_token()
    elif type.lower() == "mac":
        return fake.mac_platform_token()


def file_size(size: str, output: str, char: str = "a") -> str:
    return fake.file_size(size, output, char)
