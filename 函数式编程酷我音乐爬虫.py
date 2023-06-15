# 访问链接
import requests
# 进度条
from tqdm import tqdm
# 把url转换成json格式的数据
def url_json(url):
    """
    将url链接用json进行解析
    :param url: 歌曲的网址
    :return: json数据
    """
    headers = {
        'Cookie': '_ga=GA1.2.1065701725.1684117448; _gid=GA1.2.207714512.1684117448; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1684117448,1684118602; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1684118602; kw_token=IZHLKUXE23M',
        'Referer': 'https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%B7%B1',
        'csrf': 'IZHLKUXE23M',
        'Host': 'www.kuwo.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
    }
    res = requests.get(url=url, headers=headers).json()
    return res
# 拿到歌曲的访问链接
def url_list(url_json):
    """
    将json数据进行解包
    :param url_json: json数据
    :return: 两个可迭代对象
    """
    lists = url_json['data']['list']
    for i in lists:
        # 获取遍历出来的音乐信息
        rid = i['rid']
        artist = i['artist']
        name = i['name']
        info = '{} {}'.format(artist, name)
        mp3_url = f'https://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
        print('歌曲的访问链接为：{}'.format(mp3_url))
        print('歌曲是：{}'.format(info))
        yield mp3_url
        yield info
# 把接收到的链接转换成int类型数据
def url_bytes(mp3_url):
    """
    把链接转换成int型数据
    :param mp3_url: 歌曲访问链接
    :return: 歌曲下载链接
    """
    res = requests.get(mp3_url).json()
    url_json = res['data']['url']
    print('歌曲的下载链接为：{}'.format(url_json))
    res_url = requests.get(url_json, stream=True)
    return res_url
def mp3_open(url_bytes, mp3_info):
    """
    把歌曲写入到本地
    :param url_bytes: int型数据
    :param mp3_info: 歌手名，歌曲名
    :return: 0
    """
    conte_size = int(url_bytes.headers['content-length']) / 1024
    with open('{}.mp3'.format(mp3_info), 'wb') as f:
        # f.write(url_bytes)
        for i in tqdm(iterable=url_bytes.iter_content(1024),
                      total=conte_size,
                      unit='kb',
                      desc='下载中...'):
            f.write(i)
        print('下行完成!')
        return 0
def main():
    """
    程序总函数
    :return: 0
    """
    # 通过输入的歌曲名获取音乐列表链接
    a  = input('请输入歌曲名称：')
    url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={a}&pn=1&rn=20&httpsStatus=1&reqId=83069ca0-f2e3-11ed-b9e6-3d0d95dbf491'
    # 将链接里的内容转换成json型数据
    list_json = url_json(url)
    # 通过遍历拿出歌曲信息，然后转换成生成器函数
    mp3_url = url_list(list_json)
    # 获取音乐id
    v1 = next(mp3_url)
    # 获取歌手名，歌曲名
    v2 = next(mp3_url)
    # 写入本地
    res_url = url_bytes(v1)
    mp3_open(res_url, v2)
    return 0
main()