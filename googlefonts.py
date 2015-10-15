from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import requests
import re

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

s = requests.Session()
s.mount('https://', MyAdapter())
cssFileUri="https://fonts.googleapis.com/css?family=Roboto:400,400italic,700,900,700italic,900italic,500,500italic,300italic,300,100italic,100"

# 获取css文本
def getCSSFile(uri):
    r=requests.get(uri)
    if r.status_code==200:
        return r.text

def getFontUris(content):
    regex = re.compile(r'url\((https[^\)]*?)\)', re.IGNORECASE)
    return regex.findall(content)

def download(url):
    r=requests.get(url)
    with open(url.split('/')[-1], 'wb') as fd:
        for chunk in r.iter_content(1024):
            fd.write(chunk)
        fd.close()

content=getCSSFile(cssFileUri)

if content is not None:
    uriList=getFontUris(content)
    for u in uriList:
        download(u)
    print (uriList)
