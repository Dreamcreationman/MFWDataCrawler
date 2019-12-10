import hashlib
import requests
from bs4 import BeautifulSoup

def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]

page_total = 1
sid = 2618773
page = 2
t = 1553500557401
qdata = '{"_ts":"'+str(t)+'","params":"{\\"poi_id\\":\\"'+ str(sid) +'\\",\\"page\\":' + \
    str(page)+',\\"just_comment\\":1}"}c9d6618dbc657b41a66eb0af952906f1'
sn = par(qdata.encode('utf-8'))
url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
querystring = {"callback": "jQuery181011036861119045205_1553502048335",
                "params": "%7B%22poi_id%22%3A%22{}%22%2C%22page%22%3A{}%2C%22just_comment%22%3A1%7D".format(str(sid), str(page)),
                "_ts": t,
                "_sn": sn,
                "_": t+1}
headers = {
    'Referer': "http://www.mafengwo.cn/poi/"+str(sid)+".html",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
for key, value in querystring.items():
    url = url+key+'='+str(value)+'&'
url = url[:-1]
response = requests.request("GET", url, headers=headers)
data = response.text.encode('utf-8').decode("unicode_escape")
data = data.replace("<\/", "</")
header_idx = data.find('"html":"') + 8
content = data[header_idx:].split('<div align="right" class="m-pagination">')[0]
print(data)
page = data[header_idx:].split('<div align="right" class="m-pagination">')[1].split("</div>")[0]

soup = BeautifulSoup(page, "html.parser")
with open("data.html", "w", encoding="utf-8") as fop:
    fop.write(page)
page_total = int(str(soup.find("span", {"class": "count"}).find("span").text))

soup = BeautifulSoup(content, "html.parser")
for comment in soup.find_all("li", {"class": "rev-item comment-item clearfix"}):
    user_avatar = comment.find("div", {"class": "user"}).find("a", {"class": "avatar"}).find("img")["src"]
    user_level = str(comment.find("div", {"class": "user"}).find("span", {"class": "level"}).text).split(".")[1]
    user_name = comment.find("a", {"class": "name"}).text
    user_comment = comment.find("p", {"class": "rev-txt"}).text
    user_comment_time = comment.find("div", {"class": "info clearfix"}).find("span", {"class": "time"}).text
    user_star = comment.find("span", {"class": "s-star"})["class"][1][-1:]
    print(user_avatar+", "+user_level+", "+str(user_name)+", "+str(user_comment)+", "+str(user_comment_time).replace(",", "，").strip().strip("\n")+", "+str(user_star))
    break