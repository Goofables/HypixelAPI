from json import load
from pprint import pprint

import requests

# output = load(open("sellToShop.json", 'r'))
# for k in output:
#     output[k] = -1
# with open("sellToShop.json", 'w') as outfile:
#     dump(output, outfile)
# exit()
key = next(iter(load(open("apikeys.json")).values()))

buyFromShop = load(open("buyFromShop.json", 'r'))
sellToShop = load(open("sellToShop.json", 'r'))
merch = load(open("merchantSellValues.json", 'r'))
list = requests.get("https://api.hypixel.net/skyblock/bazaar/products?key=" + key).json()
items = load(open("items.json", 'r'))
if not list["success"]:
    print("Could not get new list!")
    print(list["cause"])
    exit()

for item in items:
    if item not in list["productIds"]:
        print(f"-{item}")
for item in list["productIds"]:
    if item not in items:
        print(f"+{item}")

pprint(list["productIds"])

# for item in list["productIds"]:
#     sellShop = -1
#     buyShop = -1
#     name = "XXXXXXXXXXXXXXXXXXXX"
#     if item in buyFromShop:
#         buyShop = buyFromShop[item]
#     if item in sellToShop:
#         sellShop = sellToShop[item]
#     if item in merch:
#         sellShop = merch[item]["merchSellValue"]
#         name = merch[item]["name"]
#     itemsOut[item] = {
#         "name": name,
#         "buyFromShop": buyShop,
#         "sellToShop": sellShop,
#         "recipe": {},
#         "confirmed": False
#     }
#     if item in sellToShop and sellShop != sellToShop[item] and sellToShop[item] != -1:
#         print(f"{item}: {sellShop} <> {sellToShop[item]}")
#
# for item in merch:
#     if item not in list["productIds"]:
#         print("-" + item)
#
# with open("items.json", 'w') as outfile:
#     dump(itemsOut, outfile)
