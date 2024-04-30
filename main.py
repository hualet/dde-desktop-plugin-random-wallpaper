#!/usr/bin/env python3

import os
import json
import string
import requests
import random
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
        print("exception in get_random_wallpaper_360: ", e)
        return None


def get_random_wallpaper_codelife():
    wallpaper = None
    try:
        data = requests.get("https://api.codelife.cc/wallpaper/random").json()
        if data["code"] == 200:
            wallpaper = data["data"]
        return wallpaper
    except Exception as e:
        print("exception in get_random_wallpaper_codelife: ", e)
        return None

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


# 根据输入的URL，通过requests库下载URL对应的壁纸到/temp目录，并返回该壁纸的路径
def download_wallpaper(url):
    try:
        response = requests.get(url)
        wallpaper_name = "random_wallpaper_" + generate_random_string(5)

        # TODO(hualet): don't know how to get file name correctly.
        # if response.status_code == 200 and 'Content-Disposition' in response.headers:
        #     content_disposition = response.headers['Content-Disposition']
        #     if content_disposition:
        #         file_name_parts = content_disposition.split('filename=')
        #         if len(file_name_parts) == 2:
        #             wallpaper_name = file_name_parts[1].strip('"')
        #         else:
        #             print("Invalid Content-Disposition format:", content_disposition)
        #     else:
        #         print("Content-Disposition is null")

        filename = '/tmp/' + wallpaper_name
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        print("exception in download_wallpaper: ", e)
        return None


def set_wallpaper(path):
    try:
        command = 'qdbus com.deepin.daemon.Appearance /com/deepin/daemon/Appearance com.deepin.daemon.Appearance.SetCurrentWorkspaceBackground {}'.format(path)
        print("set wallpaper: ", command)
        os.system(command)
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    wallpaper = get_random_wallpaper_codelife()
    if not wallpaper:
        wallpaper = get_random_wallpaper_360()
    print("ramdom wallpaper url: ", wallpaper)

    if wallpaper:
        uri = download_wallpaper(wallpaper)
        if uri:
            set_wallpaper(uri)