## CHECK
## https://hypixel-skyblock.fandom.com/wiki/Minions
##

import re
from json import load, loads, dump
from pprint import pprint

minions = load(open("minions.json", 'r'))
items = load(open("sellToShop.json", 'r'))

times = minions["time"]
storage = minions["storage"]
resources = minions["resources"]
tmp = {}
for l in times.split('\n'):
    name = l.split(":")[0]
    tmp[name] = {}
    arr = loads(l.split(":")[1].replace("Unknown", "-1"))
    tmp[name]["time"] = arr
for l in storage.split('\n'):
    name = l.split(":")[0]
    arr = loads(l.split(":")[1].replace("Unknown", "-1"))
    tmp[name]["storage"] = arr
for l in resources.split('\n'):
    name = l.split(":")[0]
    res = loads("{ \"res\":" + re.sub(r"([a-zA-Z0-9-]+)", r'"\1"', l.split(":")[1]) + "}")
    tmp[name]["resources"] = res['res']

# pprint(tmp)
for name in tmp:
    minions[name] = {}
    minions[name]["resources"] = {}
    minions[name]["levels"] = {}
    for r in tmp[name]["resources"]:
        item_name = ""
        r = r.replace("-", "_")
        for i in items:
            if "ENCHANTED" in i:
                continue
            if r.upper() in i:
                if r.upper() == i or "_ITEM" in i:
                    item_name = i
                    break
                print(f"{r}: `{i}`")
        if item_name is "":
            item_name = r
        if item_name.islower():
            print(f"X: {item_name}")
            minions[name]["resources"]["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"] = -1
        minions[name]["resources"][item_name] = 1
    for i in range(11):
        minions[name]["levels"][str(i)] = {
            "time": tmp[name]["time"][i],
            "storage": tmp[name]["storage"][i]
        }
pprint({})
# pprint(minions)
with open("minions.json", 'w') as outfile:
    dump(minions, outfile)

## CHECK
## https://hypixel-skyblock.fandom.com/wiki/Minions
##
