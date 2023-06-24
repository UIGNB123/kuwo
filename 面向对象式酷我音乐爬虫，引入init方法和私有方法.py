# 访问链接
import requests
# 进度条
from tqdm import tqdm
# 定义一个类来构造方法
class Music:
    def __init__(self):
        """
        通过用户输入的歌曲名搜索对应的音乐列表
        :return: 歌曲列表链接
        """
        a = input('请输入想要下载的歌曲名称：')
        url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={a}&pn=1&rn=20&httpsStatus=1&reqId=83069ca0-f2e3-11ed-b9e6-3d0d95dbf491'
        self.__url_json(url)
    def __url_json(self, url):
        """
        将搜索到的链接进行响应
        :return: 放回一个json型数据
        """
        headers = {
            'Cookie': '_ga=GA1.2.1065701725.1684117448; _gid=GA1.2.207714512.1684117448; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1684117448,1684118602; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1684118602; kw_token=IZHLKUXE23M',
            'Referer': 'https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%B7%B1',
            'csrf': 'IZHLKUXE23M',
            'Host': 'www.kuwo.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
        }
        res = requests.get(url=url, headers=headers).json()
        self.__url_list(res)
    def __url_list(self, res):
        """
        只获取音乐列表里的第一首歌曲
        :return: 返回这首歌曲的音乐信息和通过音乐id获取的链接
        """
        lists = res['data']['list']
        for i in lists:
            # 获取遍历出来的音乐信息
            rid = i['rid']
            artist = i['artist']
            name = i['name']
            info = '{} {}'.format(artist, name)
            mp3_url = f'https://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
            print('歌曲的访问链接为：{}'.format(mp3_url))
            print('歌曲是：{}'.format(info))
            self.__url_bytes(info, mp3_url)
            break
    def __url_bytes(self, info, mp3_url):
        """
        通过外链获取音乐的播放链接并使用tqdm对链接进行转换
        :return:返回tqdm转换之后的数据
        """
        res = requests.get(mp3_url).json()
        url_json = res['data']['url']
        print('歌曲的下载链接为：{}'.format(url_json))
        res_url = requests.get(url_json, stream=True)
        self.__mp3_open(info, res_url)
    def __mp3_open(self, info, res_url):
        """
        将数据转换成二进制数据然后写入本地
        :return:
        """
        conte_size = int(res_url.headers['content-length']) / 1024
        with open('{}.mp3'.format(info), 'wb') as f:
            # f.write(url_bytes)
            for i in tqdm(iterable=res_url.iter_content(1024),
                          total=conte_size,
                          unit='kb',
                          desc='下载中...'):
                f.write(i)
            print('下行完成!')
# 创建一个对象，让它来进行音乐的下载，就是这么简单
music = Music()