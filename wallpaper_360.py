
import requests
import json
from random import randint
from pprint import pprint

def get_random_wallpaper():
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
