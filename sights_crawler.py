import requests
from bs4 import BeautifulSoup
import csv

querystring = []
payload = ""
HEADERS = {
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

def get_conent(destination_id, payload, headers, querystring):
    url = "http://www.mafengwo.cn/jd/" + destination_id + "/gonglve.html"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    data = response.text
    return data

def get_info(sight_id):
    url = "http://www.mafengwo.cn/poi/5015.html"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    data = response.text
    return data

def get_destination_id():
    destination_ids = []
    with open("destination.csv", "r", encoding="utf-8") as fop:
        reader = csv.reader(fop)
        next(reader)
        for row in reader:
            destination_ids.append(row[0])
    return destination_ids

if __name__ == "__main__":
    with open("sights.csv", "w", encoding="utf-8") as sig_fop:
        sig_fop.write("des_id, sight_id, name, num_comment, description\n")
        des_ids = get_destination_id()
        for did in des_ids:
            res = get_conent(did, payload, HEADERS, querystring)
            soup  = BeautifulSoup(res, "html.parser")
            sights = soup.find("div", {"data-cs-p": "必游景点", "class": "row row-top5"})
            if sights == None:
                continue
            for sight in sights.find_all("div", {"class":"item clearfix"}):
                href = sight.find("div", {"class":"middle"}).find("h3").find("a")["href"]
                name = sight.find("div", {"class":"middle"}).find("h3").find("a")["title"]
                print(did+":"+name)
                num_comment = ""
                try:
                    num_comment = sight.find("div", {"class":"middle"}).find("h3").find("a").find("a").find("em").text
                except AttributeError:
                    num_comment = "0"
                description = sight.find("div", {"class":"middle"}).find("p").text
                sig_fop.write(did+", "+str(href).strip().strip("\n")[5:-5]+", "+str(name).strip().strip("\n")+", "+str(num_comment).strip().strip("\n")+", "+str(description).strip().strip("\n")+"\n")