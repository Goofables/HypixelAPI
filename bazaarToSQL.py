from json import load, loads
from time import sleep

import pymysql
import requests

creds = load(open("sql.json"))
key = next(iter(load(open("apikeys.json")).values()))

# Initialize db connection
db = pymysql.connect(
    host=creds["host"],
    user=creds["username"],
    passwd=creds["password"],
    db=creds["database"]
)
last_update = 0
n = 0
with db.cursor() as cursor:
    while True:
        if n > 10000:
            n = 0
            db.close()
            db = pymysql.connect(
                host=creds["host"],
                user=creds["username"],
                passwd=creds["password"],
                db=creds["database"]
            )
            cursor = db.cursor()
        n += 1
        sleep(7)
        # sleep(2)
        try:
            bazaar = loads(requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + key).text)
            if "lastUpdated" not in bazaar:
                continue
            thisUpdate = int(bazaar["lastUpdated"] / 10000) * 10
            sql = "INSERT INTO `bazaarupdate` (`time`) VALUES (FROM_UNIXTIME(%s))"
            if last_update == thisUpdate:
                continue
            last_update = thisUpdate
            cursor.execute(sql, last_update)
            cursor.execute("SELECT LAST_INSERT_ID()")
            updateId = cursor.fetchone()[0]

            sql = "INSERT INTO bazaaritem (update_id, item_id, instant_sell, instant_buy, sell_order, buy_order) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            for item in bazaar["products"]:
                cursor.execute("SELECT id FROM items WHERE item_name = %s", item)
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO `items` (`item_name`, `name`) VALUES (%s, %s)", (item, item))
                    cursor.execute("SELECT LAST_INSERT_ID()")
                itemId = cursor.fetchone()[0]

                buyList = bazaar["products"][item]["buy_summary"]
                sellList = bazaar["products"][item]["sell_summary"]
                # print(f"{item}: {buyList} {sellList}")
                if len(buyList) > 0:
                    buyList = buyList[0]["pricePerUnit"]
                else:
                    buyList = -1
                if len(sellList) > 0:
                    sellList = sellList[0]["pricePerUnit"]
                else:
                    sellList = -1
                cursor.execute(sql, (updateId, itemId, bazaar["products"][item]["quick_status"]["sellPrice"],
                                     bazaar["products"][item]["quick_status"]["buyPrice"], sellList, buyList))
            db.commit()
            print(f"Updated at: {last_update}")
        except Exception as e:
            print(item)
            print(e)
