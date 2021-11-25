from json import load
from datetime import datetime, timedelta
import time
import pymysql

creds = load(open("sql.json"))
items = load(open("items.json", 'r'))

db = pymysql.connect(
    host=creds["host"],
    user=creds["username"],
    passwd=creds["password"],
    db=creds["database"]
)
start = time.time()
yesterday = (datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0)
# yesterday = datetime(year=2020, month=12, day=31, hour=0, minute=0, second=0, microsecond=0)
yesterday2 = yesterday + timedelta(seconds=59)
timefmt = "%Y-%m-%d %H:%M:%S"

cursor = db.cursor()
sql = "SELECT MIN(time) FROM bazaarupdate"
cursor.execute(sql)
begining = cursor.fetchone()[0]
timedif = timedelta(minutes=1)
day = 1

sql = "SELECT count(id) FROM bazaarupdate"
cursor.execute(sql)
totalUpdates = cursor.fetchone()[0]
sql = "SELECT count(*) FROM bazaaritem"
cursor.execute(sql)
totalItems = cursor.fetchone()[0]

while yesterday2 >= begining:
    sql = "SELECT MIN(update_id), MAX(update_id), item_id, AVG(instant_sell), Avg(instant_buy), AVG(sell_order), " \
          "AVG(buy_order) FROM `bazaaritem` WHERE `update_id` IN (SELECT id FROM bazaarupdate " \
          "WHERE `time` BETWEEN %s AND %s) GROUP BY item_id;"
    cursor.execute(sql, (yesterday.strftime(timefmt), yesterday2.strftime(timefmt)))
    rows = cursor.fetchall()
    rowMax = -1
    rowMin = -1
    for row in rows:
        if row[0] < rowMin or rowMin == -1:
            rowMin = row[0]
        if row[1] > rowMax or rowMax == -1:
            rowMax = row[1]

    if rowMax != rowMin:
        print(f"Combine Minute: {yesterday.strftime(timefmt)}")
        sql = "UPDATE bazaaritem SET " \
              "update_id = %s, instant_sell = %s, instant_buy = %s, sell_order = %s, buy_order = %s " \
              "WHERE update_id = %s and item_id = %s"
        for row in rows:
            update_id = row[0]
            item_id = row[2]
            iSell = row[3]
            iBuy = row[4]
            SellO = row[5]
            BuyO = row[6]
            # print(sql % (rowMin, iSell, iBuy, SellO, BuyO, update_id, item_id))
            cursor.execute(sql, (rowMin, iSell, iBuy, SellO, BuyO, update_id, item_id))

        sql = "DELETE FROM bazaarupdate WHERE id = %s"
        for rowId in range(rowMin + 1, rowMax + 1):
            cursor.execute(sql, rowId)

    sql = "UPDATE bazaarupdate SET time = %s WHERE id = %s"
    cursor.execute(sql, (yesterday.strftime(timefmt), rowMin))

    db.commit()

    if day == 1:
        if yesterday + timedelta(days=2) < datetime.now():
            day = 2
            timedif = timedelta(minutes=10)
            yesterday = yesterday.replace(minute=0)
            yesterday2 = yesterday2.replace(minute=9)
    elif day == 2:
        if yesterday + timedelta(days=3) < datetime.now():
            day = 3
            timedif = timedelta(hours=1)
            yesterday = yesterday.replace(minute=0)
            yesterday2 = yesterday2.replace(minute=59)

    yesterday = yesterday - timedif
    yesterday2 = yesterday2 - timedif
print("Done deleting!")
print("Cleaning up...")
sql = "SELECT MAX(id) FROM bazaarupdate"
cursor.execute(sql)
maxId = cursor.fetchone()[0]
sql = "SELECT id FROM bazaarupdate AS A WHERE (SELECT id FROM bazaarupdate AS B WHERE B.id = A.id + 1) IS NULL ORDER BY id ASC LIMIT 1"
cursor.execute(sql)
minId = cursor.fetchone()[0]
sql = "SET @i = %s"
cursor.execute(sql, minId - 1)
sql = "UPDATE bazaarupdate SET id=(@i := @i + 1) WHERE id BETWEEN %s AND %s"
for i in range(minId, maxId, 1000):
    print(f"{i}/{maxId}")
    cursor.execute(sql, (i, i + 999))
sql = "ALTER TABLE bazaarupdate AUTO_INCREMENT = 0"
cursor.execute(sql)

sql = "SELECT count(id) FROM bazaarupdate"
cursor.execute(sql)
totalUpdates = totalUpdates - cursor.fetchone()[0]
sql = "SELECT count(*) FROM bazaaritem"
cursor.execute(sql)
totalItems = totalItems - cursor.fetchone()[0]

print(f"Deleted: {totalItems} records {totalUpdates} updates")
cursor.close()
print(f"Total time: {time.time() - start}")
"""  
0: 10s
1: 1m
2: 10m
3: 1h
"""