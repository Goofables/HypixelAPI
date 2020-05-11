from json import load

import requests

key = next(iter(load(open("apikeys.json")).values()))

items = load(open("items.json", 'r'))
bazaar = requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + key).json()

matches = 0
profitItems = {}
for product in bazaar["products"]:
    if product not in items or items[product]["buyFromShop"] < 0:
        continue
    bazaarSell = bazaar["products"][product]["quick_status"]["sellPrice"]
    if items[product]["buyFromShop"] >= bazaarSell:
        continue
    name = items[product]["name"]
    if "XXXXX" in name:
        name = product
    profitItems[matches] = {
        "name": name,
        "bazaar": bazaarSell,
        "shop": items[product]["buyFromShop"],
        "profit": bazaarSell - items[product]["buyFromShop"],
        "markup": (bazaarSell / items[product]["buyFromShop"] - 1) * 100
    }
    matches += 1

for product in range(matches):
    for b in range(0, matches - product - 1):
        if profitItems[b]["markup"] < profitItems[b + 1]["markup"]:
            profitItems[b], profitItems[b + 1] = profitItems[b + 1], profitItems[b]

for itemNumber in profitItems:
    item = profitItems[itemNumber]
    print(
        f"{item['name']}: {round(item['bazaar'], 2)} - {round(item['shop'], 2)} = {round(item['profit'], 2)} ({round(item['markup'], 2)}%)")

print(matches)
