from lxml import etree
import requests
import re
url = 'https://www.toopic.cn/'
res = requests.get(url)
# res.encoding = 'utf-8'

obj = re.compile(r'<a href=(.*?)target="_blank" class="pic">')
resp = re.findall(obj, res.text)
i = 0
for item in resp:
    item = item.replace('','').replace('"', '')
    urls = url + item
    jpg = urls.split('/')[-1]
    
    res_p = requests.get(urls)
    et = etree.HTML(res_p.text)
    objc = et.xpath('//img/@src')

    dic = {}
    for jpg_item in objc:
        i += 1
        jpg_url = url + jpg_item
        jpg = jpg_url.split('/')[-1]
        dic[i] = jpg_url
        print(i, jpg_url)
    try:
        j = input('请输入要下载的序列号:')
        if dic[int(j)].split('.')[-1] == 'jpg':
            print('可以下载')
            print(dic[int(j)])
            dow = requests.get(dic[int(j)]).content

            with open(f'D:\Python学习\图片\{jpg}', 'wb')as f:
                f.write(dow)
        else:
            print('文件格式错误，无法进行下载')
            print('程序已退出')
            break
    except Exception:
        print('输入的序列号有误')
        print('程序已退出')
        break
