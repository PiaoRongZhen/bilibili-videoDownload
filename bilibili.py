# -*- coding: utf-8 -*-
# Author : PiaoRongZhen

import requests, json, re
from contextlib import closing


pc_browser_headers = {
        # 伪装PC浏览器
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        # 防御式编程
        'Referer': 'https://www.bilibili.com/'
}

# video_url视频下载地址
# video_name视频名称
def video_downloader(video_url, video_name):

    with closing(session.get(video_url, headers = pc_browser_headers, stream=True)) as response:

        if response.status_code == 200:
            
            # 视频大小
            content_size = int(response.headers['content-length'])
            print('[文件大小]:', round(content_size / 1024 / 1024, 2), 'MB')
            
            # 视频保存路径
            video_name = 'D:/' + video_name
            
            # 写文件
            with open(video_name, 'wb') as file:
                size = 0
                for data in response.iter_content(chunk_size = 1024):
                    file.write(data)
                    size += len(data)
                    print('[下载进度]' + str(round(size / content_size * 100, 2)) + '%', end='\r')
                    
        else:
            print('链接异常')


# 测试地址
url = 'https://www.bilibili.com/video/av10859730'


session = requests.Session()

# 获取视频页面html文档
response = session.get(url=url, headers=pc_browser_headers)

# 使用正则表达式提取视频信息 （json格式）
pattern = '__playinfo__=(.*)</script><script>window'
information = re.findall(pattern, response.text)[0]

# 加载视频信息（json格式）
html = json.loads(information)
# 提取视频下载地址（视频可能分段）
durl = html['durl']
download_url = []
for i in range(len(durl)):
    download_url.append(durl[i]['url'])


# 分段下载视频
for i in range(len(download_url)):
    fileName = str(i+1) + '.flv'
    video_downloader(download_url[i], fileName)
    
print('下载完成')
    
    
    


