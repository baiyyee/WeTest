import os
from WeTest.tool import happybirthday


def test_happybirthday():
    
    birthday_infos = [
        ("张三", "农历", "3.7"),
        ("李四", "阳历", "4.18"),
        ("王五", "阳历", "4.19"),
    ]

    birthday_words = [
        "今天是个特别的日子，开心最重要哈",
        "世界因为你的存在而变得更加美好了",
        "今天更要开心鸭！",
        "今天你最大，燥起来吧",
        "你就是美好本身啊",
        "大块吃肉，大口喝酒，人生得意需尽欢",
        "你还是曾经那个少年，没有一丝丝改变",
        "愿你三冬暖，愿你春不寒。愿你天黑有灯，下雨有伞。愿你路上有良人伴",
        "你正在一点点变好，迎面吹来的风也越来越温柔",
        "一天的胡吃海喝，不耽误百年减肥大计的。今朝有酒，醉起来吧",
        "愿你的每一岁都能奔走在自己的热爱里",
        "别说话，点我！",
        "@all, 彩虹屁什么的快快吹起来呗~~",
        "愿快乐的鱼塘被你承包",
        "愿有人问你茶可温，有人与你立黄昏",
        "福如东海，寿比南山！",
    ]
    
    robot_key = os.getenv("ROBOT_KEY")
    happybirthday.happy_birthday(birthday_infos, birthday_words, robot_key)