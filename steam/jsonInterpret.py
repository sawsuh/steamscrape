import json
import math

with open('out.json') as f:
    data = json.load(f)

tuplist = []
for game in data:
    title = game["title"]
    try: 
        totalreviews = float(game["totalreviews"].replace(',',''))
        goodreviews = float(game["posreviews"].replace(',',''))
        posprop = 100*goodreviews/totalreviews
    except ValueError:
        #posprop = None
        continue
    try:
#        discountprice = float(game["discountprice"][3:])
#        oldprice = float(game["oldprice"][3:])
        price = float(game["price"][3:])
        #fraction = #100*(1 - discountprice/oldprice)
        group = math.floor(price/20)
    except ValueError:
        continue
    tuplist.append((title, group, posprop, price))

newlistIntermediate = sorted(tuplist, key = lambda x : x[2], reverse=True)
newlist = sorted(newlistIntermediate, key = lambda x : x[1])
for title, g, posprop, p in newlist:
    #if posprop:
    print(f'{title} - ${p} {posprop:.2f}%')
    #else:
        #print(f'{title} - ${p} ({frac:.2f}% off)')
