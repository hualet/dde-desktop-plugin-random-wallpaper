#!/usr/bin/env python3

import os
import json
import requests
from random import randint
from pprint import pprint

def get_random_wallpaper_360():
    try:
        data = requests.get("http://cdn.apc.360.cn/index.php?c=WallPaper&a=getAllCategoriesV2&from=360chrome").json()
        category_list = data["data"]
        random_category = category_list[randint(0, len(category_list)-1)]

        request_url = "http://wallpaper.apc.360.cn/index.php?" \
                    "c=WallPaper&a=getAppsByCategory" \
                    "&cid={cid}" \
                    "&start=0" \
                    "&from=360chrome".format(cid=random_category["id"])
        category_wallpaper_list= requests.get(request_url).json()["data"]
        random_wallpaper = category_wallpaper_list[randint(0, len(category_wallpaper_list)-1)]
        return random_wallpaper["img_1600_900"]
    except Exception as e:
        print("Error: ", e)
        return None

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
    wallpaper = get_random_wallpaper_360()
    print("ramdom wallpaper: ", wallpaper)
    if wallpaper:
        uri = download_wallpaper(wallpaper)
        if uri:
            set_wallpaper(uri)