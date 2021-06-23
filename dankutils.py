import discord, random, json, asyncio
from discord.ext import commands

class dankutils(commands.Cog, name='Dank Memer Utilities'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='heist')
	async def heist(self, ctx, sponsor:discord.Member=None, *, amount=None):
		if sponsor == None:
			await ctx.reply('Please provide a sponsor')
			return
		if amount == None:
			await ctx.reply('Please provide an Amount')
			return
		else:
			person = sponsor
			await ctx.channel.send('<@&811087619243900969>')
			embed = discord.Embed(title = 'Heist Announcement <a:Pepe_Heist:800807282014552082>', description = f'<a:arrow:823861255927365662> **Amount** - {amount}\n<a:arrow:823861255927365662> **Sponsor** - {person.mention}\n<a:arrow:823861255927365662> **Slowmode** - 5 minutes\n__**Things to do -**__\n<a:pd_Arrow:800949891093626910> Keep 2000 coins in your wallet\n<a:pd_Arrow:800949891093626910> Keep a life saver in your inventory\n<a:pd_Arrow:800949891093626910> Type only `join heist` as you get only 1 chance.\n<a:pd_Arrow:800949891093626910> Thank the sponsor in chat!', colour = discord.Color.green()).set_footer(text = 'Ready? React!')
			x = await ctx.send(embed=embed)
			await x.add_reaction('<a:Pepe_Heist:800807282014552082>')

	def get_aucs_data():
		with open("aucs.json", "r") as f:
			users = json.load(f)
		return users

	def open_auc(aucid, prize, auctioneer, sp):
		with open("aucs.json", "r") as f:
			users = json.load(f)
		if str(aucid) in users:
			return False
		else:
			users[str(aucid)] = {}
			users[str(aucid)]["sp"] = sp
			users[str(aucid)]["prize"] = prize
			users[str(aucid)]["status"] = "not started"
			users[str(aucid)]["highest_bid"] = None
			users[str(aucid)]["highest_bidder"] = None
			users[str(aucid)]["auctioneer"] = auctioneer
		with open("aucs.json", "w") as f:
			json.dump(users, f)
		return True

	@commands.command(name='auction')
	async def auction(self, ctx, startpr=None, *, items=None):
		if 'm' not in startpr or items == None:
			await ctx.reply('**Error: Incorrect Usage**\nCorrect Usage - `_auction <startprice> <items>`\nE.g. `_auction 30m 1 pepe trophy`')
			return
		with open("cooldown.json", "r") as f:
			cooldown = json.load(f)
		def open_cool(aucid):
			with open("cooldown.json", "r") as f:
				users = json.load(f)
			if str(ctx.user.id) in users:
				return False
			else:
				users[str(aucid)] = {}
				users[str(aucid)]["auction"] = 0
			with open("cooldown.json", "w") as f:
				json.dump(users, f)
			return True
		open_cool(ctx.guild.id)
		cc = cooldown[str(ctx.guild.id)]["auction"]
		if cc != 0:
			await ctx.channel.send(f"{ctx.author.mention} This command is currently on cooldown.\nWait for another {round(cc/60)} minutes to use it again.")
			return
		cooldown[str(ctx.guild.id)]["auction"] = 900
		with open("cooldown.json", "w") as f:
			json.dump(cooldown, f)
		await ctx.delete()
		aucid = random.randint(0,1000)
		msg = ctx.content.split()
		if "m" not in msg[len(msg)-1]:
			await ctx.channel.send('**Error: You used improper syntax!**\nThe correct syntax is `//auction <prize/items [e.g. 1 pepe trophy]> <starting prize in millions [e.g. for 500k, 0.5m; for 10 mil, 10m]>`\n**Note:** Do not use the < and > in the cmd. And be sure to include a `m` in the starting price')
			return
		prize = items
		open_auc(aucid, prize, message.author.id, sp)
		bb = "{:,}".format(sp*1000000)
		await ctx.send('<@&825961158250594324>')
		embed = discord.Embed(title = f"{prize} Auction", description = f"Auctioneer: {ctx.author.mention}\nStarting Prize: {bb}\nAucID: {aucid}", colour = discord.Color.green())
		embed.set_footer(text = 'Ready? React!\nUse //aucstart <aucid> to start the auction!')
		xd = await ctx.send(embed=embed)
		await xd.add_reaction('<a:pd_BanHammer:825972386679488542>')
		for i in range(900):
			cooldown[str(ctx.guild.id)]["auction"] -= 1
			with open("cooldown.json", "w") as f:
				json.dump(cooldown, f)
			await asyncio.sleep(1)

	@commands.command(aliases=["tc"])
	async def taxcalc(self, ctx,amount):
		calctax = amount /(8/100)
		newamount = amount - calctax
		neededtax = amount + calctax
		strcalc =  float(calctax)
		strneededtax = str(neededtax) 
		await ctx.send("Amount lost: " + neededtax + "\nAmount given: " + newamount + "\nAmount needed: " + calctax)
def setup(bot):
    bot.add_cog(dankutils(bot))
