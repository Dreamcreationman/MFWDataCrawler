import hashlib
import requests
from bs4 import BeautifulSoup
import csv

def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]

def get_page_total(sid):
    page = 1
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
    page = data[header_idx:].split('<div align="right" class="m-pagination">')[1].split("</div>")[0]
    soup = BeautifulSoup(page, "html.parser")
    page_total = int(str(soup.find("span", {"class": "count"}).find("span").text))
    return page_total

def get_content(sid, page):
    t = 1553500557401
    qdata = '{"_ts":"'+str(t)+'","params":"{\\"poi_id\\":\\"'+ str(sid) +'\\",\\"page\\":' + \
        str(page)+',\\"just_comment\\":1}"}c9d6618dbc657b41a66eb0af952906f1'
    sn = par(qdata.encode('utf-8'))
    URL = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
    QUERY_STRINGS = {"callback": "jQuery181011036861119045205_1553502048335",
                    "params": "%7B%22poi_id%22%3A%22{}%22%2C%22page%22%3A{}%2C%22just_comment%22%3A1%7D".format(str(sid), str(page)),
                    "_ts": t,
                    "_sn": sn,
                    "_": t+1}
    HEADERS = {
        'Referer': "http://www.mafengwo.cn/poi/"+str(sid)+".html",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    for key, value in QUERY_STRINGS.items():
        URL = URL+key+'='+str(value)+'&'
    URL = URL[:-1]
    response = requests.request("GET", URL, headers=HEADERS)
    data = response.text.encode('utf-8').decode("unicode_escape")
    data = data.replace("<\/", "</")
    header_idx = data.find('"html":"') + 8
    content = data[header_idx:].split('<div align="right" class="m-pagination">')[0]
    return content

def get_sight_id():
    sight_ids = []
    with open("sight.csv", "r", encoding="utf-8") as fop:
        reader = csv.reader(fop)
        next(reader)
        for row in reader:
            sight_ids.append(int(row[1]))
    return sight_ids

if __name__ == "__main__":
    with open("comment.csv", "w", encoding='utf8', errors='surrogatepass') as com_fop:
        com_fop.write("sight_id, user_avatar, user_level , user_name, user_comment, user_comment_time, user_star\n")
        sightids = get_sight_id()
        for sid in sightids:
            num = 1
            try:
                page_count = get_page_total(sid)
            except IndexError:
                continue
            for page in range(page_count):
                content = get_content(sid, page+1)
                soup = BeautifulSoup(content, "html.parser")
                for comment in soup.find_all("li", {"class": "rev-item comment-item clearfix"}):
                    user_avatar = comment.find("div", {"class": "user"}).find("a", {"class": "avatar"}).find("img")["src"]
                    user_level = str(comment.find("div", {"class": "user"}).find("span", {"class": "level"}).text).split(".")[1]
                    user_name = comment.find("a", {"class": "name"}).text
                    user_comment = comment.find("p", {"class": "rev-txt"}).text
                    user_comment_time = comment.find("div", {"class": "info clearfix"}).find("span", {"class": "time"}).text
                    user_star = comment.find("span", {"class": "s-star"})["class"][1][-1:]
                    try:
                        print(num, sid, page+1, page_count, user_name, user_star)
                    except UnicodeEncodeError:
                        pass
                    com_fop.write(str(sid)+", "+user_avatar+", "+user_level+", "+str(user_name)+", "+"".join(str(user_comment).replace("\n", "。").replace(",", "，").strip().strip("\n").split())+", "+str(user_comment_time)+", "+str(user_star)+"\n")
                    num += 1