import requests
from bs4 import BeautifulSoup

URL = "http://www.mafengwo.cn/mdd/base/list/pagedata_citylist"
querystring = []
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

def get_content(url, page, headers, querystring):
    payload = "mddid=12703&page=" + str(page) + "&_ts=1575861622281&_sn=5e8352f015"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    data = response.text.encode('utf-8').decode("unicode_escape")
    return data

def process_data(response):
    footer_flag = '","page":"'
    footer_idx = response.find(footer_flag)
    if footer_idx != -1:
        list_content = response[9:footer_idx]
        list_content = list_content.replace("<\/", "</")
        list_content = list_content.strip("\n")
        return list_content
    else:
        print("cannot find footer flag!")
        return None

if __name__ == "__main__":
    with open("destination.csv", "w", encoding="utf-8") as des_fop:
        des_fop.write("id, name, img, num_people, detail\n")
        for i in range(15):
            response = get_content(URL, i+1, HEADERS, querystring)
            processed_data = process_data(response)
            soup = BeautifulSoup(processed_data,  "html.parser")
            sights = soup.find_all("li", {"class":"item"})
            for sight in sights:
                data_id = sight.find("a")['data-id']
                img = sight.find("a").find("img")['data-original']
                name = sight.find("a").find("div", {"class":"title"}).text.replace('"', "")
                num_people = sight.find("dl", {"class":"caption"}).find('dt').find('div', {"class":"nums"}).find("b").text
                detail = sight.find("dl", {"class":"caption"}).find('dt').find('div', {"class":"detail"}).text
                des_fop.write(str(data_id).strip()+", "+str(name.strip().split(" ")[0]).strip()+", "+str(img).strip()+", "+str(num_people).strip()+", "+str(detail.replace(",","，")).strip().strip("\n")+"\n")