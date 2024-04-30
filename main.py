#!/usr/bin/env python3

import os
import requests
from wallpaper_360 import get_random_wallpaper

# 根据输入的URL，通过requests库下载URL对应的壁纸到/temp目录，并返回该壁纸的路径
def download_wallpaper(url):
    try:
        response = requests.get(url)
        wallpaper_name = url.split('/')[-1]
        if response.status_code == 200:
            filename = '/tmp/' + wallpaper_name
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print("Error: ", e)
        return None


def set_wallpaper(path):
    try:
        command = 'qdbus com.deepin.daemon.Appearance /com/deepin/daemon/Appearance com.deepin.daemon.Appearance.SetCurrentWorkspaceBackground {}'.format(path)
        print("set wallpaper: ", command)
        os.system(command)
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    wallpaper = get_random_wallpaper()
    print("ramdom wallpaper: ", wallpaper)
    if wallpaper:
        uri = download_wallpaper(wallpaper)
        if uri:
            set_wallpaper(uri)