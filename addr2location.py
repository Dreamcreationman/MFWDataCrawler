import requests
import MySQLdb
import json

AK = "t2GfuAwsM1LWkbNkCntslV8S8SGlDdtb"

def get_all_sights(conn, cursor):
    sql = "select id, location from vis_sig"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        conn.rollback()
        return None

def update_sight_info(conn, sight_id, latitude, longitude, types):
    sql = "UPDATE vis_sig SET longitude=%s, latitude=%s, type=%s WHERE id = %s"
    values = (longitude, latitude, types, sight_id)
    try:
        cur.execute(sql, values)
        conn.commit()
    except:
        conn.rollback()
    

if __name__ == "__main__":
    conn = MySQLdb.Connect(host = '127.0.0.1',
                        port = 3306,
                        user = 'root',
                        passwd = 'hty5469449464',
                        db = 'mafengwo',
                        charset='utf8')
    cur = conn.cursor()

    sights = get_all_sights(conn, cur)
    for row in sights:
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + row[1] + "&output=json&ak=" + AK
        response = requests.get(url)
        info = json.loads(response.text)
        longitude = info["result"]["location"]["lng"]
        latitude = info["result"]["location"]["lat"]
        types = info["result"]["level"]
        update_sight_info(conn, row[0], latitude, longitude, types)
        print(row[0], latitude, longitude, types)

    conn.close()