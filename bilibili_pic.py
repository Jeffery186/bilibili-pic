import json
import os.path
import time

import requests
import yaml

with open('conf.yaml', 'r') as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)
    url = "https://api.vc.bilibili.com/link_draw/v1/doc/others"

    data = {
        "biz": 0,
        "poster_uid": conf['BILIBILIPIC']['POSTER_UID'],
        "page_num": 0,
        "page_size": 45
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
        "Referer": "https://space.bilibili.com"
    }

    cookies_dict = {
        "SESSDATA": conf['BILIBILIPIC']['SESSDATA']
    }

    res = requests.get(url=url, params=data, headers=headers, cookies=cookies_dict).content
    res_decode = res.decode('utf-8')
    res_json = json.loads(res_decode)

    head_url = res_json['data']['user']['head_url']
    head_url_str = str(head_url)
    head_url_name = head_url_str.split("/")[5]

    print(head_url_name)

    pic_path = res_json['data']['user']['name']
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
        os.chdir(pic_path)
    else:
        os.chdir(pic_path)

    head_url_res = requests.get(url=head_url, headers=headers)
    with open(head_url_name, "wb") as f1:
        f1.write(head_url_res.content)

    items = res_json['data']['items']

    for i in range(0, 44):
        item = items[i]['pictures']
        lens = len(item) - 1
        print(lens)
        if lens == 0:
            img_src_url = item[0]['img_src']
            # print(item)
            print(img_src_url)
            img_src_str = str(img_src_url)
            img_src_name = img_src_str.split("/")[5]
            img_src_res = requests.get(url=img_src_url, headers=headers)
            with open(img_src_name, "wb") as f2:
                f2.write(img_src_res.content)
        else:
            for j in range(0, lens):
                img_src_url = item[j]['img_src']
                # print(item)
                print(img_src_url)
                img_src_str = str(img_src_url)
                img_src_name = img_src_str.split("/")[5]
                img_src_res = requests.get(url=img_src_url, headers=headers)
                with open(img_src_name, "wb") as f3:
                    f3.write(img_src_res.content)
        time.sleep(1)
    print('下载完成')
