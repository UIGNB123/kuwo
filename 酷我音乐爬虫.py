# 导入访问链接的模块
import requests
a = input('输入歌曲名称：')
url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={a}&pn=1&rn=20&httpsStatus=1&reqId=25afcea0-f3f1-11ed-934b-5744fc6c792e'
# 防盗协议
headers = {
    'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1684242631; _ga=GA1.2.2139569368.1684242631; _gid=GA1.2.1733794304.1684242631; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1684245245; _gat=1; kw_token=VJFRXEZ91LQ',
    'csrf': 'VJFRXEZ91LQ',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%B7%B1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'
}
# 响应链接
res = requests.get(url, headers=headers).json()
# print(res)
# 获取音乐列表
res_url = res['data']['list']
i = 0
for mu in res_url:
    i += 1
    # 歌曲名称
    artist = mu['artist']
    # 专辑名称
    album = mu['album']
    # 歌手名称
    name = mu['name']
    # 歌曲id
    rid = mu['rid']
    # 每首歌曲对应的访问链接
    rid_url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
    # 转换成json型数据
    mp3_url = requests.get(rid_url).json()
    # 获取MP3链接
    music_data = mp3_url['data']['url']
    # 输出歌曲性息
    music_url = '{}.{} {}'.format(artist, album, name)
    print(music_url)
    # 转换成字节码文件
    data_url = requests.get(music_data).content
    # 写入本地
    with open('{}.mp3'.format(name), 'wb') as f:
        f.write(data_url)
    break
print('下载成功')


