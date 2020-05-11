from json import load

import pymysql

creds = load(open("sql.json"))
items = load(open("items.json", 'r'))

db = pymysql.connect(
    host=creds["host"],
    user=creds["username"],
    passwd=creds["password"],
    db=creds["database"]
)
with db.cursor() as cursor:
    # cursor.execute("DELETE FROM items WHERE 1")
    # cursor.execute("ALTER TABLE items AUTO_INCREMENT = 0")
    sql = "INSERT INTO `items` (`item_name`, `name`, `sellToShop`, `buyFromShop`) VALUES (%s, %s, %s, %s)" \
          "ON DUPLICATE KEY UPDATE `name` = %s, `sellToShop` = %s, `buyFromShop` = %s;"
    for item in items:
        print(f"{item}:{items[item]['name']} Sell:{items[item]['sellToShop']} Buy:{items[item]['buyFromShop']}")
        cursor.execute(sql, (item, items[item]["name"], items[item]["sellToShop"], items[item]["buyFromShop"],
                             items[item]["name"], items[item]["sellToShop"], items[item]["buyFromShop"]))
        db.commit()
