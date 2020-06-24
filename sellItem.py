from json import load
from pprint import pprint

import requests

pprint({})
key = next(iter(load(open("apikeys.json")).values()))

items = load(open("items.json", 'r'))
bazaar = requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + key).json()

matches = 0
profitItems = {}
target = input("Item name: ")
for product in bazaar["products"]:
    if product not in items:
        continue
    if not (target.upper() in product or target.upper() in items[product]["name"].upper()):
        continue
    name = items[product]["name"]
    if "XXXX" in name:
        name = product
    profitItems[matches] = {
        "name": name,
        "bazaar": bazaar["products"][product]["quick_status"]["sellPrice"],
        "shop": items[product]["sellToShop"]
    }
    matches += 1

for itemNumber in profitItems:
    item = profitItems[itemNumber]
    print(
        f"{item['name']}: Bazaar: {round(item['bazaar'], 2)} Shop: {round(item['shop'], 2)}")

print(matches)
