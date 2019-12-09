import requests
from bs4 import BeautifulSoup

url = "http://www.mafengwo.cn/jd/10061/gonglve.html"
querystring = []
payload = ""
headers = {
    'Pragma': "no-cache",
    'Origin': "http://www.mafengwo.cn",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/java, */*; q=0.01",
    'Cache-Control': "no-cache",
    'X-Requested-With': "",
    'Referer': "http://www.mafengwo.cn/mdd/citylist/12703.html",
    'cache-control': "no-cache",
    'Postman-Token': "74506c28-c314-4238-b55d-b781360f6a2d"
}
response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
data = response.text

with open("original.html", "w", encoding="utf-8") as fop:
    fop.write(data)