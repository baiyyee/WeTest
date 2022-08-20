import sxtwl
import random
import requests
from datetime import datetime


lunar = sxtwl.Lunar()

ymc = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rmc = [day for day in range(1, 32)]


def happy_birthday(birthday_infos: list, birthday_words: list, robot_key: str):

    members = []

    for birthday_info in birthday_infos:

        today = datetime.now().date()
        name, type, birthday = birthday_info

        birthday_month, birthday_day = birthday.split(".")

        today = lunar.getDayBySolar(today.year, today.month, today.day)

        current_month, current_day = today.m, today.d

        if type in ["阴历", "农历"] and not today.Lleap:
            current_month, current_day = ymc[today.Lmc], rmc[today.Ldi]

        if int(birthday_month) == current_month and int(birthday_day) == current_day:
            members.append(name)

    # Maybe 1 more guys share the same day as their birthday
    if len(members) >= 1:
        names = ", ".join(members)
        birthday_word = random.choice(birthday_words)
        send_message(names, birthday_word, robot_key)


def send_message(name: str, birthday_word: str, robot_key: str):

    api = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_key}"
    headers = {"Content-Type": "application/json"}
    image = "http://bpic.588ku.com/element_origin_min_pic/16/11/25/5dc79ecbdc2faf630cd68b4e241f2224.jpg"

    payload = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": f"{name}, 生日快乐！",
                    "description": f"{birthday_word}",
                    "url": "http://www.taobao.com/",
                    "picurl": f"{image}",
                }
            ]
        },
    }

    requests.post(url=api, headers=headers, json=payload)
