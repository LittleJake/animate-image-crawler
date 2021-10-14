UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
     " Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31"

RULE = {
    'safebooru': {
        'url': 'https://safebooru.org/index.php?page=post&s=list&tags=',
        'url_reg': 'src=\"(.+[A-Za-z0-9]{40}.jpg\?\d+)\"',
        'name_reg': '[a-zA-Z0-9]{40}'
    },
    'gelbooru': {
        'url': 'https://gelbooru.com/index.php?page=post&s=list&tags=',
        'url_reg': 'src=\"(.+[A-Za-z0-9]{32}.jpg\?*\d*)\"',
        'name_reg': '[a-zA-Z0-9]{32}'
    }
}

THREAD_NUM = 16
OUTPUT = './download/'
EXT = ['.jpg', '.png', '.jpeg', '.gif', '.webm']
NUM = 40
SITE = 'safebooru'
LOG_FORMAT = "[%(asctime)s] %(message)s"
LOG_LEVEL = 20
