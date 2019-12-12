import hashlib
import requests
from bs4 import BeautifulSoup

sid = 5015

url = "http://www.mafengwo.cn/poi/"+ str(5015) +".html"
querystring = {}
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Connection":"keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cookie": "__jsluid_h=166423c12deec81310ab1a96369ec59f; mfw_uuid=5deafdf8-c60e-efbb-2600-ae2ea5ba06a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-12-07+09%3A18%3A48%22%3B%7D; uva=s%3A91%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1575681530%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22http%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1575681530%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5deafdf8-c60e-efbb-2600-ae2ea5ba06a6; UM_distinctid=16eddf01a994a2-03914a61701cb7-3963720f-1fa400-16eddf01a9aa33; __omc_chl=; __mfwothchid=referrer%7Cblog.csdn.net; __mfwc=referrer%7Cblog.csdn.net; __omc_r=; _r=0; __mfwlv=1576134719; __mfwvn=12; CNZZDATA30065558=cnzz_eid%3D672699475-1575676940-http%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1576133600; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A19%3A%22127.0.0.1%2Fdata.html%22%3Bs%3A1%3A%22t%22%3Bi%3A1576135738%3B%7D; PHPSESSID=9905m32j8iqflsnibj03foebk3; __jsl_clearance=1576138914.248|0|BJbT82pkAEmTTUxBtc9zeOKEQ10%3D; __mfwa=1575681529462.36378.19.1576134719260.1576138916484; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1575801424,1575810620,1576134719,1576138917; __mfwb=7dc58cbeb6a8.7.direct; __mfwlt=1576138932; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1576138933"
}
response = requests.request("GET", url, headers=headers)
data = response.text
print(data)
# with open("data.html", "w", encoding="utf-8") as fop:
#     fop.write(data)

soup = BeautifulSoup(data, "html.parser")
summary = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("div", {"class": "summary"}).text
summary = "".join(str(summary).replace(",", "，").split()).replace("·","")
phone = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "tel"}).find("div", {"class": "content"}).text
site = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "item-site"}).find("div", {"class": "content"}).find("a").text
duration = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "item-time"}).find("div", {"class": "content"}).text
open_time = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find_all("dl")[2].find("dd").text
open_time = "".join(str(open_time).replace(",", "，").split()).replace("·","")
location = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-location"}).find("div", {"class": "mhd"}).find("p", {"class": "sub"}).text
print(summary+", "+ phone+ ", "+ site + ", "+ duration+ ", "+ open_time+ ", "+ location)