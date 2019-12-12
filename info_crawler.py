import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Connection":"keep-alive",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cookie": "__jsluid_h=166423c12deec81310ab1a96369ec59f; mfw_uuid=5deafdf8-c60e-efbb-2600-ae2ea5ba06a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-12-07+09%3A18%3A48%22%3B%7D; uva=s%3A91%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1575681530%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22http%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1575681530%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5deafdf8-c60e-efbb-2600-ae2ea5ba06a6; UM_distinctid=16eddf01a994a2-03914a61701cb7-3963720f-1fa400-16eddf01a9aa33; __omc_chl=; __mfwothchid=referrer%7Cblog.csdn.net; __mfwc=referrer%7Cblog.csdn.net; __omc_r=; _r=0; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A19%3A%22127.0.0.1%2Fdata.html%22%3Bs%3A1%3A%22t%22%3Bi%3A1576135738%3B%7D; PHPSESSID=9905m32j8iqflsnibj03foebk3; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1575801424,1575810620,1576134719,1576138917; __mfwa=1575681529462.36378.20.1576138916484.1576142852421; __mfwlv=1576142852; __mfwvn=13; CNZZDATA30065558=cnzz_eid%3D672699475-1575676940-http%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1576144400; RT=\"sl=6&ss=1576144539877&tt=117253&obo=1&sh=1576145428766%3D6%3A1%3A117253%2C1576145174886%3D5%3A1%3A105968%2C1576145066883%3D4%3A1%3A87446%2C1576144999930%3D3%3A1%3A20505%2C1576144620082%3D2%3A0%3A20505&dm=mafengwo.cn&si=70k6ile4bjv&rl=1&ld=1576145428766&r=http%3A%2F%2Fwww.mafengwo.cn%2Fpoi%2F5015.html&ul=1576145603167&hd=1576145604119\"; __jsl_clearance=1576146953.916|0|Esy3ojDH0QWOX%2BiGppRj3dFz4vA%3D; __mfwb=dac48ace1d85.34.direct; __mfwlt=1576147835; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1576147836"
}

def get_data(sight_id, headers):
    proxies_me = {
        "http":"socks5://127.0.0.1:1080",
        "https":"socks5://127.0.0.1:1080"
    }
    url = "http://www.mafengwo.cn/poi/"+ str(int(sight_id)) +".html"
    response = requests.request("GET", url, headers=headers)
    data = response.text
    return data

if __name__ == "__main__":
    with open("sights.csv", "r", encoding="utf-8") as fr:
        reader = csv.reader(fr)
        with open("sight.csv", "w", encoding="utf-8") as fw:
            head = fr.readline();
            i = 1
            fw.write(head.strip()+",summary, phone, site, duration, open_time, location\n")
            for row in reader:
                data = get_data(row[1], HEADERS)
                soup = BeautifulSoup(data, "html.parser")
                
                summary = ""
                try:
                    summary = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("div", {"class": "summary"}).text
                    summary = "".join(str(summary).replace(",", "，").split()).replace("·","")
                except AttributeError :
                    pass    

                phone = ""
                try:
                    phone = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "tel"}).find("div", {"class": "content"}).text
                except AttributeError :
                    pass

                site = ""
                try:
                    site = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "item-site"}).find("div", {"class": "content"}).find("a").text
                except AttributeError :
                    pass

                duration = ""
                try:
                    duration = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find("ul", {"class": "baseinfo clearfix"}).find("li", {"class": "item-time"}).find("div", {"class": "content"}).text
                except AttributeError :
                    pass

                open_time = ""
                try:
                    open_time = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-detail"}).find_all("dl")[-1].find("dd").text
                    open_time = "".join(str(open_time).replace(",", "，").split()).replace("·","")
                except AttributeError or IndexError:
                    pass
                except IndexError:
                    pass

                location = ""
                try:
                    location = soup.find("div", {"data-anchor": "overview"}).find("div", {"class": "mod mod-location"}).find("div", {"class": "mhd"}).find("p", {"class": "sub"}).text
                except AttributeError :
                    pass
                fw.write(",".join(row) +","+ summary+", "+ phone+ ", "+ site + ", "+ duration+ ", "+ open_time+ ", "+ location+"\n")
                i = i + 1
                print(row[1], phone)