import json
def getbal(balid):
	try:
		with open('data/accounts.json') as f:
			amounts = json.load(f)
			print("Successfully loaded amounts.json")
		if balid not in amounts.keys():
			amounts[balid] = 100
			save(amounts,balid)
		if amounts[balid] <= 0:
			amounts[balid] = 0
			save(amounts, balid)
		print(amounts.get(balid))
		return amounts[balid]
				
	except FileNotFoundError:
		return print("Could not load amounts.json")

def save(amts,savid):
	with open('data/accounts.json', 'w+') as f:
		amounts = json.load(f)
		json.dump(amts, f)