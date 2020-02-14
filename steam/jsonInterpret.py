import json

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
        posprop = None
        pass
    try:
        discountprice = float(game["discountprice"][3:])
        oldprice = float(game["oldprice"][3:])
        fraction = 100*(1 - discountprice/oldprice)
    except ValueError:
        continue
    tuplist.append((title, fraction, posprop, discountprice))

newlist = sorted(tuplist, key = lambda x : x[1], reverse=True)
for title, frac, posprop, p in newlist:
    if posprop:
        print(f'{title} - ${p} {posprop:.2f}% ({frac:.2f}% off)')
    else:
        print(f'{title} - ${p} ({frac:.2f}% off)')
