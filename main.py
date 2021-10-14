#!/usr/bin/python3
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
import urllib3
import re
import sys
import ssl
from utils import Config
import random

executor = ThreadPoolExecutor(Config.THREAD_NUM)
# Disable ssl warning. (Why not?)
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE, retries=3, timeout=10, num_pools=64, maxsize=64)

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def download_and_save(url, header, name):
    downloaded = False
    for ext in Config.EXT:
        response = http.request(method="GET",
                                url=url.replace(".jpg", ext),
                                headers=header)
        if response.status == 200:
            path = Config.OUTPUT + "/" + name + ext
            with open(path, 'wb') as fp:
                fp.write(response.data)
                fp.flush()
            logging.info("{} {}".format("save to:", path))
            downloaded = True
            break

    if not downloaded:
        logging.info("{} {} {}".format(url, response.status, 'failed.'))


def crawl(tags):
    rule = Config.RULE.get(Config.SITE, None)
    if rule is None:
        logging.error("{} {} {}".format("Site", Config.SITE, "not supported."))
        exit(-1)
    page = 0
    while True:
        # Common booru site url schema.
        url = rule.get('url') + " ".join(tags) + '&pid=' + str(Config.NUM * page)
        response = http.request(method="GET",
                                url=url,
                                headers={'User-Agent': Config.UA})
        s = str(response.data, encoding='utf-8')
        header = {'User-Agent': Config.UA, 'Referer': url}
        images = re.findall(rule.get('url_reg'), s)
        for img in images:
            # Rip for original size url from the url of the thumbnail.
            img = img.replace("thumbnails", "images").replace("thumbnail_", "")
            # Get the fixed unique name of the image for saving and judging the existed image.
            name = re.findall(rule.get('name_reg'), img)[0]
            downloaded = False
            for ext in Config.EXT:
                path = Config.OUTPUT + name + ext
                if os.path.exists(path):
                    downloaded = True
                    break

            if downloaded:
                logging.warning("{} {}".format("Exist:", path))
                continue
            # Submit to ThreadPool for downloading.
            executor.submit(download_and_save, img, header, name)
            # Ease the load of the image server.
            time.sleep(random.randint(1, 2))

        # If no more images on the page.
        if images is None or len(images) == 0:
            logging.warning('No more image to download.')
            logging.warning('If this is the first page, please check the tags name or check for the script update.')
            return

        page = page + 1
        logging.info("{} {}".format("Fetching no.", page * Config.NUM))


def print_help():
    print("Usage: main.py <arguments>")
    print("Example: main.py --tag='megumin'"
          " --tags='kono_subarashii_sekai_ni_shukufuku_wo! megumin'"
          " --site='gelbooru' --thread-num=8")

    print("")
    print("Arguments:")
    print("--tags='<tag names>': Multiple tag names. Each tag name separate by space. "
          "Replace space with underscore in one single tag.")
    print("--tag='<tag name>'  : Single tag name. Can implement several times.")
    print("--site=<site name>  : (Optional) Site name. Currently safebooru and gelbooru supported. default='safebooru'")
    print("--output=<path>     : (Optional) Output directory path. default='./download/'")
    print("--thread-num=<num>  : (Optional) How many downloads allow at the same time. default=16")


tags = set()
for v in sys.argv[1:]:
    if len(v.split("=", 1)) == 2:
        _k, _v = v.split("=", 1)
        _k = _k.lstrip("-")
        if _k == 'tag':
            tags.add(_v.strip('"').strip("'").replace(' ', '_'))
        elif _k == 'tags':
            tags = tags.union(set(_v.strip('"').strip("'").split(" ")))
        else:
            setattr(Config, _k.upper().replace("-", "_"), _v.strip('"').strip("'"))

if len(tags) == 0:
    print_help()
    exit(-1)

logging.info("{} {} {} {}".format('Fetching tags', tags, 'from site', Config.SITE))
crawl(tags)
