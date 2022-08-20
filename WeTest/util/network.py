import requests
from user_agents import parse
from ipaddress import ip_address
from ..const import API_IP_QUERY
from urllib.parse import urlparse, ParseResult


def get_domain(url: str) -> str:
    
    return parse_url(url).netloc


def parse_url(url: str) -> ParseResult:
    
    return urlparse(url)


def get_ip_by_range(start_ip: str, end_ip: str) -> str:
    
    start = int(ip_address(start_ip).packed.hex(), 16)
    end = int(ip_address(end_ip).packed.hex(), 16) + 1

    return [ip_address(ip).exploded for ip in range(start, end)]


def parse_ip(ip: str) -> dict:
    
    url = API_IP_QUERY.format(ip=ip)
    data = requests.get(url).json()["data"]

    result = {
        "ip": data["ip"],
        "isp": data["isp"],
        "region": data["region"],
        "country_id": data["country_id"],
        "country": data["country"],
        "city": data["city"],
    }

    return result


def parse_useragent(useragent: str) -> dict:
    
    parsed_ua = {}
    user_agent = parse(useragent)

    is_mma = user_agent.is_mobile or user_agent.is_tablet

    parsed_ua["is_mma"] = is_mma
    parsed_ua["user_agent"] = useragent
    parsed_ua["browser_name"] = user_agent.browser.family.replace("Other", "Unknown")
    parsed_ua["browser_version"] = user_agent.browser.version_string or "Unknown"
    parsed_ua["system_name"] = user_agent.os.family.replace("Other", "Unknown")
    parsed_ua["system_version"] = (
        "{} {}".format(user_agent.os.family, user_agent.os.version_string).strip().replace("Other", "Unknown")
    )

    if user_agent.is_pc:
        parsed_ua["platform"] = "DSK"
        parsed_ua["device"] = "DSK"
    else:
        parsed_ua["platform"] = "MBL"
        parsed_ua["device"] = "PHN"

    return parsed_ua


def get_url_params(url: str) -> dict:
    
    params = {}
    for param in url.split("&"):
        if "=" in param:
            key, value = tuple(param.split("="))
            params[key] = value

    return params
