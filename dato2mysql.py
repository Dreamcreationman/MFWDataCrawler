import MySQLdb
import csv

conn = MySQLdb.Connect(host = '127.0.0.1',
                        port = 3306,
                        user = 'root',
                        passwd = 'hty5469449464',
                        db = 'mafengwo',
                        charset='utf8')
cur = conn.cursor()

# with open("destination.csv", "r", encoding="utf-8") as fop:
#     reader = csv.reader(fop)
#     next(reader)
#     for row in reader:
#         into = "INSERT INTO vis_des(id, name, img, num, detail) VALUES (%s,%s, %s, %s, %s)"
#         values = (row[0],row[1],row[2],row[3],row[4])
#         cur.execute(into, values)
#         conn.commit()

# with open("sight.csv", "r", encoding="utf-8") as fop:
#     reader = csv.reader(fop)
#     next(reader)
#     for row in reader:
#         try:
#             into = "INSERT INTO vis_sig(id, des_id, name, num_comment, desp, summary, phone, site, duration, open_time, location) VALUES (%s,%s, %s, %s, %s,%s,%s, %s, %s, %s, %s)"
#             values = (row[1],row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
#             cur.execute(into, values)
#             conn.commit()
#         except MySQLdb._exceptions.IntegrityError:
#             continue

with open("comment.csv", "r", encoding="utf-8", errors='surrogatepass') as fop:
    reader = csv.reader(fop)
    next(reader)
    for row in reader:
        print(row[0],row[1],row[2],row[3])
        try:
            into = "INSERT INTO vis_com(sig_id, avatar, level, username, comment, time, star) VALUES (%s, %s, %s, %s,%s,%s,%s)"
            values = (row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            cur.execute(into, values)
            conn.commit()
        except MySQLdb._exceptions.IntegrityError:
            continue

conn.close()