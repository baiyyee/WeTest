import os
import imgkit
import base64
import hashlib
import requests


headers = {"Content-Type": "application/json"}
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"


def send_text(key: str, content: str):
    
    payload = {"msgtype": "text", "text": {"content": content}}
    requests.post(url=url.format(key=key), headers=headers, json=payload)


def send_markdown(key: str, content: str):
    
    payload = {"msgtype": "markdown", "markdown": {"content": content}}
    requests.post(url=url.format(key=key), headers=headers, json=payload)


def send_image(key: str, image_path: str):
    
    with open(image_path, "rb") as f:
        image_base64 = str(base64.b64encode(f.read()), encoding="utf-8")
        image_md5 = hashlib.md5()
        image_md5.update(base64.b64decode(image_base64))
        image_md5 = image_md5.hexdigest()

    payload = {"msgtype": "image", "image": {"base64": image_base64, "md5": image_md5}}
    requests.post(url=url.format(key=key), headers=headers, json=payload)


def send_news(key: str, title: str, description: str, url: str, picurl: str):
    
    payload = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": f"{title}",
                    "description": f"{description}",
                    "url": f"{url}",
                    "picurl": f"{picurl}",
                }
            ]
        },
    }

    requests.post(url=url.format(key=key), headers=headers, json=payload)


def send_file(key: str, path: str):
    
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"

    files = {"file": open(path, "rb")}
    media_id = requests.post(url=url.format(key=key), files=files).json()["media_id"]

    payload = {"msgtype": "file", "file": {"media_id": media_id}}
    requests.post(url=url.format(key=key), headers=headers, json=payload)


def send_html(key: str, path: str):
    
    """Send html report as jpg and file"""

    jpg_path = path.replace(".html", ".jpg")

    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["DISPLAY"] = ":0.0"

    options = {"encoding": "UTF-8"}

    imgkit.from_file(path, jpg_path, options=options)

    send_image(key, jpg_path)
    send_file(key, path)
