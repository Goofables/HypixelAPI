from json import dump, load

import requests

# output = load(open("sellToShop.json", 'r'))
# for k in output:
#     output[k] = -1
# with open("sellToShop.json", 'w') as outfile:
#     dump(output, outfile)
# exit()
key = next(iter(load(open("apikeys.json")).values()))

output = load(open("buyFromShop.json", 'r'))
newList = requests.get("https://api.hypixel.net/skyblock/bazaar/products?key=" + key).json()

if not newList["success"]:
    print("Could not get new list!")
    print(newList["cause"])
    exit()

print("Checking to add")
added = 0
for i in newList["productIds"]:
    if i not in output:
        output[i] = -1
        added += 1
        print("+" + i)

print("Checking to remove")
toRemove = 0
max = 0
for i in output:
    if len(i) > max:
        max = len(i)
    if i not in newList["productIds"]:
        toRemove += 1
        print("-" + i)
print(f"Max: {max}")
print("Checking enchanted updates")
enchantedModifier = 32 * 5
for i in output:
    if output[i] <= 0:
        continue
    ench = "ENCHANTED_" + i
    if ench in output:
        amt = output[i] * enchantedModifier
        if output[ench] != amt:
            # output[ench] = amt
            print(f"{i}:{output[i]} => {ench}:{output[ench]}")

print(f"New: {added}")
print(f"To remove: {toRemove}")
if added > 0:
    with open("buyFromShop.json", 'w') as outfile:
        dump(output, outfile)
