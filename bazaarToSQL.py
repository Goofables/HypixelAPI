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
while True:
    sleep(5)
    bazaar = loads(requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + key).text)
    with db.cursor() as cursor:
        lastUpdated = bazaar["lastUpdated"]
        sql = "INSERT INTO `bazaarupdate` (`time`) VALUES (FROM_UNIXTIME(%s))"
        try:
            cursor.execute(sql, (lastUpdated / 1000))
        except pymysql.err.IntegrityError:
            continue
        cursor.execute("SELECT LAST_INSERT_ID()")
        updateId = cursor.fetchone()[0]
        sql = "INSERT INTO bazaaritem (update_id, item_id, instant_sell, instant_buy, sell_order, buy_order) " \
              "VALUES (%s, (SELECT id FROM items WHERE item_name = %s), %s, %s, %s, %s)"
        for item in bazaar["products"]:
            buyList = bazaar["products"][item]["buy_summary"]
            sellList = bazaar["products"][item]["sell_summary"]
            if len(buyList) > 0:
                buyList = buyList[0]["pricePerUnit"]
            else:
                buyList = -1
            if len(sellList) > 0:
                sellList = sellList[0]["pricePerUnit"]
            else:
                sellList = -1
            cursor.execute(sql, (updateId, item, bazaar["products"][item]["quick_status"]["sellPrice"],
                                 bazaar["products"][item]["quick_status"]["buyPrice"], sellList, buyList))
    db.commit()
    print(f"Updated at: {lastUpdated}")
