# Python 爬虫
# 爬取网易云音乐
import requests  # 请求模块 用Python模拟浏览器向服务器发起请求
from bs4 import BeautifulSoup  # 筛选数据的

# 1.确定 获取网址
url = "https://y.music.163.com/m/artist?id=1030001"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
res = requests.get(url=url, headers=headers)

# 3.筛选数据  xpath  re json bs4 pyquery
# 数据预处理   获取整体界面
soup = BeautifulSoup(res.text, 'html.parser')

# 匹配对应的数据,音乐名称
result = soup.find('ul', class_='f-hide')

infor = result.find_all('a')

idlist = []  # 存放ID

namelist = []  # 存放名字

number = 0  # 歌曲的序号

for i in infor:
    # 歌曲序号
    number = number + 1

    name = i.text  # 音乐名字

    # <a href="/song?id=1917957092">爱</a>
    result = i.get('href')
    # result结果就是href后边的数据值

    # /song?id=1917957092
    id = result[9:]
    idlist.append(id)

    Newurl = 'https://music.163.com/' + result
    namelist.append(name)
    print(str(number) + ' ' + name + ' ' + Newurl)
    # 4.保存数据 ()[]{}


def download():

        a = input("请输入你要下载的歌曲的序号:")
        b = int(a) - 1
        aa = idlist[b]
        musicName = namelist[b]

        url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(aa)
        music = requests.get(url=url, headers=headers).content

        with open('{}.mp3'.format(musicName), 'wb') as f:
            f.write(music)
            print(musicName + '下载完毕!')


download()

