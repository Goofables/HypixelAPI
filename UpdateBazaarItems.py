from json import dump, load

import requests

key = next(iter(load(open("apikeys.json")).values()))

output = load(open("prices.json", 'r'))
newList = requests.get("https://api.hypixel.net/skyblock/bazaar/products?key=" + key).json()

if not newList["success"]:
    print("Could not get new list!")
    print(newList["cause"])
    exit()

added = 0
for i in newList["productIds"]:
    if i not in output:
        output[i] = -1
        added += 1
        print("+" + i)

toRemove = 0
for i in output:
    if i not in newList["productIds"]:
        toRemove += 1
        print("-" + i)

print(f"New: {added}")
print(f"To remove: {toRemove}")

if added > 0:
    with open("prices.json", 'w') as outfile:
        dump(output, outfile)
