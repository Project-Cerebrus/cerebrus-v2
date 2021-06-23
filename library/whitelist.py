import discord, requests, asyncio, random, json

def getlist():
	with open("data/whitelist.json","r") as f:
		users = json.load(f)
	return users
def checklist(name,id):
	whitelist = getlist()
	if str(id) in whitelist:
		return "Enjoy premnium"
	else:
		return 1
def add2list(name,id):
	whitelist = getlist()
	if str(id) in whitelist:
		return "Already there"
	else:
		whitelist[str(id)] = {}
		whitelist[str(id)]["name"] = str(name)
		with open("data/whitelist.json","w") as f:
			json.dump(whitelist,f)
async def resetcd(ctx,id,name):
	try:
		whitelist = getlist()
		if str(id) in whitelist:
			print(f"[Whitelist]: {name}")
			ctx.command.reset_cooldown(ctx)
			return
	except KeyError:
		return