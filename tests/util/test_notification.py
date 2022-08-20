import os
import requests
from lxml import etree
from pathlib import Path
from datetime import datetime
from WeTest.util import notification


# Work Wechat robot key
key = os.getenv("ROBOT_KEY")


def test_send_text():

    notification.send_text(key, "Hello World!")


def test_send_markdown():

    content = """实时新增用户反馈<font color="warning">132例</font>，请相关同事注意。\n
        >类型:<font color="comment">用户反馈</font> \n
        >普通用户反馈:<font color="comment">117例</font> \n
        >VIP用户反馈:<font color="comment">15例</font>
"""

    notification.send_markdown(key, content)


def test_send_image(tmp_path: Path):

    image = requests.get("https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png").content
    path = tmp_path / "test.jpg"
    path.write_bytes(image)

    notification.send_image(key, str(path))


def test_send_news():

    time = datetime.now().strftime("%b.%d %A")
    url = "http://wufazhuce.com/"
    response = requests.get(url=url)
    html = etree.HTML(response.text)

    word = html.xpath('//*[@id="carousel-one"]/div/div[1]/div[2]/div[2]/a/text()')[0]
    picurl = html.xpath('//*[@id="carousel-one"]/div/div[1]/a/img/@src')[0]

    notification.send_news(key, time, word, url, picurl)


def test_send_file(tmp_path: Path):

    path = tmp_path / "test.txt"
    path.write_text("Hello World!")
    notification.send_file(key, str(path))


def test_send_html(tmp_path: Path):

    content = """
        <html>
        <head>    
        <meta charset="UTF-8">    
        <title>Title</title>
        <head/>
        
        <body>
        <h1>这是一级标题</h1>
        <h2>这是二级标题</h2>
        <h3>这是三级标题</h3>
        <h4>这是四级标题</h4>
        <h5>这是五级标题</h5>
        <h6>这是六级标题</h6>
        </body>
        </html>
    """
    path = tmp_path / "test.html"
    path.write_text(content)
    notification.send_html(key, str(path))
