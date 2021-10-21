# Animate Image Crawler
![license](https://img.shields.io/github/license/LittleJake/animate-image-crawler)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/LittleJake/animate-image-crawler/build)
![requirement](https://img.shields.io/badge/python-%3E=3.0-blue)


A crawl for booru site. (gelbooru and safebooru, etc.)

动漫图片爬虫，部分站点NSFW，经请留意。



## Site Support 网站支持

| Site      | Supported | Comment          |
| --------- | --------- | ---------------- |
| Safebooru | ✔         | SFW              |
| Gelbooru  | ✔         | NSFW（18+）      |
| Konachan  | Upcoming  | SFW、NSFW（18+） |


目前支持Gelbooru和Safebooru，估计之后会添加Konachan。

目测是同一个网站框架，直接加对应网站正则表达式配置即可。



## Requirement 必须组件

1. Python3
2. Urllib3



## Usage 使用方法

```shell
# install dependency
pip3 install -r requirements.txt

# run
python3 main.py <arguments>
```

```
Usage: main.py <arguments>
Example: main.py --tag='megumin' --tags='kono_subarashii_sekai_ni_shukufuku_wo! megumin' --site='gelbooru' --thread-num=8

Arguments:
--tag='<tag name>'  : Single tag name. Can implement several times.
--tags='<tag names>': Multiple tag names. Each tag name separate by space. Replace space with underscore in one single tag.

--log-level=<num>   : (Optional) 10-DEBUG,20-INFO,30-WARNING,40-ERROR,50-CRITICAL. default=20
--output=<path>     : (Optional) Output directory path. default='./download/'
--site=<site name>  : (Optional) Site name. Currently safebooru and gelbooru supported. default='safebooru'
--thread-num=<num>  : (Optional) How many downloads allow at the same time. default=16
```



## License 开源许可

[Apache2.0](LICENSE)
