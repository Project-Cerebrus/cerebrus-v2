import discord, random
from discord.ext import commands
import os
import subprocess
import pickle
import asyncio
import json
from library.whitelist import getlist, add2list, resetcd
from discord.ext.commands import Cog 
from cogs.misc.modulus import checkpkg
devs = ['775198018441838642', '746904488396324864', '750755612505407530','793344086311698442']
from datetime import datetime
mainshop = [{"name":"Watch","price":100,"description":"Check the Time duh"},
			{"name":"Laptop","price":1000,"description":"`_pm` access"},
			{"name":"Worldwalker","price":100000,"description":"allows you to walk worlds"},
			{"name":"PC","price":10000,"description":"Gaming"},
			{"name":"Blobo","price":99999,"description":"This thing? Idk wth it is"},
			{"name":"Lebi's_ice","price":10000000000000000000000000000000000000000000,"description":"duh lebi's ice heh"}]
#block users from eco mod
blockedusers = []

def blockuser(id):
	bl.append(id)
	os.system("rm -rf data/blockedusers.dat")
	pickle.dump(blockedusers,open("data/blockedusers.dat", "wb"))
	pickle.dump(bl,open("data/blockedusers.dat", "wb")) 

try:
	bl = pickle.load(open("data/blockedusers.dat","rb"))
except FileNotFoundError:
	print("run _blockeco <id> to start blockeconomy module")

# just some card config


class economy(commands.Cog, name='Economy'):
	def __init__(self, bot):
		self.bot = bot
		cards = []
		
	@commands.command(aliases=["lod"])
	async def lifeordeath(self,ctx,user=None):
		member = "None"
		if user == "help":
			embed = discord.Embed(title="Life or death rules",description="You have 2 decks, a life deck and a death deck. 3 Cards will be randomly dealt out. If any of those cards are in your life deck, they get multiplied by 2, if in death they get multiplied by -1.5. The highest total wins.",color=discord.Color.green())
			await ctx.send(embed=embed)
			return
		pcards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
		if user == discord.Member:
			await ctx.send("WIP")
			return
		#else:
		ai1 = random.choice(pcards)
		ai2 = random.choice(pcards)
		ai3 = random.choice(pcards)
		ai4 = random.choice(pcards)
		ai5 = random.choice(pcards)
		ai6 = random.choice(pcards)
		c1 = random.choice(pcards)
		c2 = random.choice(pcards)
		c3 = random.choice(pcards)
		c4 = random.choice(pcards)
		c5 = random.choice(pcards)
		c6 = random.choice(pcards)
		embed = discord.Embed(title="Life or death",description=f"**Death Deck:**\n{c1} | {c2} | {c3}\n**Life Deck:**\n{c4} | {c5} | {c6}",color=discord.Color.green())
		await ctx.send(embed=embed)
		await ctx.send("You have **10** seconds before the death cards are dealt")
		await asyncio.sleep(10)
		d1 = random.choice(pcards)
		d2 = random.choice(pcards)
		d3 = random.choice(pcards)
		if c1 == d1 or c1 == d2 or c1 == d3:
			c1 = -1.5*c1
		if c2 == d1 or c2 == d2 or c2 == d3:
			c2 = -1.5*c2
		if c3 == d1 or c3 == d2 or c3 == d3:
			c3 = -1.5*c3
		if c4 == d1 or c4 == d2 or c4 == d3:
			c4 = 2*c4
		if c5 == d1 or c5 == d2 or c5 == d3:
			c5 = 2*c4
		if c6 == d1 or c6 == d2 or c6 == d3:
			c6 = 2*c4
		if ai1 == d1 or ai1 == d2 or ai1 == d3:
			ai1 = -1.5*ai1
		if ai2 == d1 or ai2 == d2 or ai2 == d3:
			ai2 = -1.5*ai2
		if ai3 == d1 or ai3 == d2 or ai3 == d3:
			ai3 = -1.5*ai3
		if ai4 == d1 or ai4 == d2 or ai4 == d3:
			ai4 = 2*ai4
		if ai5 == d1 or ai5 == d2 or ai5 == d3:
			ai5 = 2*ai4
		if ai6 == d1 or ai6 == d2 or ai6 == d3:
			ai6 = 2*ai4
		total = c1 + c2 + c3 + c4 + c5 + c6
		aitotal = ai1 + ai2 + ai3 + ai4 + ai5 + ai6
		embed = discord.Embed(title="Death Cards",description=f"{d1} | {d2} | {d3}",color=discord.Color.green())
		await ctx.send(embed=embed)
		if total > aitotal:
			embed = discord.Embed(title = "You won",description=f"Your total: `{total}`\nBot total: `{aitotal}`",color=discord.Color.green())
			await ctx.send(embed=embed)
			return
		if aitotal > total:
			embed = discord.Embed(title = "You lost",description=f"Your total: `{total}`\nBot total: `{aitotal}`",color=discord.Color.red())
			await ctx.send(embed=embed)
			return
		if aitotal == total:
			embed = discord.Embed(title = "You Drew",description=f"Your total: `{total}`\nBot total: `{aitotal}`",color=ctx.author.color)
			await ctx.send(embed=embed)
			return
	@commands.command()
	async def inject(self,ctx,user:discord.Member,amount: int):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		users = await get_bank_data()
		if str(ctx.author.id) in devs:
			users[str(user.id)]["wallet"] += amount
			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
			await ctx.send("Injected cash")
		else:
			await ctx.send("Devs only, stay away")
	@commands.command()
	async def whitelist(self,ctx,user:discord.Member):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		add2list(user.name,user.id)
		await ctx.send("Whitelisted")
	@commands.command()
	async def kill(self,ctx,user:discord.Member):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		kill_messages = [
			f'{ctx.author.name} killed {user.name} with a baseball bat', 
			f'{ctx.author.name} killed {user.name} with a frying pan', f'{ctx.author.name} killed {user.name} by showing their ugly face', f'{ctx.author.name} wreckt {user.name} by being a builder', f'{ctx.author.name} murdered {user.name} in cold blood', f'{ctx.author.name} showed {user.name} a tiktok', f'{ctx.author.name} got killed by {user.name} by nosebleed got a bit excited eh'
    ]  # This is where you will have your kill messages. Make sure to add the mentioning of the author (ctx.message.author.mention) and the member mentioning (member.mention) to it
		await ctx.send(random.choice(kill_messages))
	@commands.command()
	async def scout(self,ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		scout_locations = ["hell","sea","minecraft","discord","wtfisthis","DMs","dank memer","github","google bank","temple","desert","area51","bitcoin","wallet","bank","litecoin","kaneki's room","eris's bag"]
		l1 = random.choice(scout_locations)
		l2 = random.choice(scout_locations)
		l3 = random.choice(scout_locations)
		await ctx.send(f"Scout locations:\n`{l1}` | `{l2}` | `{l3}`")
		choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
		print(choice.content)
		user = ctx.author
		if choice.content.lower() == l1:
			users = await get_bank_data()

			earnings = random.randrange(101)

			await ctx.send(f'{ctx.author.mention} scouted {l1} for {earnings}')

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)

		if choice.content.lower() == l2:
			users = await get_bank_data()

			earnings = random.randrange(101)

			await ctx.send(f'{ctx.author.mention} risked their lives to steal {earnings} from {l2}')

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
		
		if choice.content.lower() == l3:
			users = await get_bank_data()

			earnings = random.randrange(101)

			await ctx.send(f'{ctx.author.mention} got {earnings} in a godly way by decmiating {l3}')

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
	@commands.command(aliases=["pm"])
	async def postmemes(self,ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		amount = 1
		item = "Laptop"
		res = await check(ctx.author,item,amount)

		if not res[0]:
			if res[1]==1:
				await ctx.send("That Object isn't there!")
				return
			if res[1]==2:
				await ctx.send(f"You don't have a laptop in your bag.")
				return
			if res[1]==3:
				await ctx.send(f"You don't have a laptop in your bag.")
				return
		await ctx.send("WIP")
	@commands.command(aliases=["hl"])
	async def highlow(self,ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		number = random.randrange(1,101)
		hint = random.randrange(1,101)
		embed = (discord.Embed(title = "highlow",description = f"your hint is **{str(hint)}**\npick wether is is `high`, `low` or `same` than a random number",color=discord.Color.green()))
		await ctx.send(embed=embed)
		choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
		print(choice.content)
		user = ctx.author
		if choice.content.lower() == "high":
			if number < hint:
				users = await get_bank_data()

				earnings = random.randrange(101)

				await ctx.send(f"You guessed right and earned {earnings}\nthe number was {str(number)}")


				users[str(user.id)]["wallet"] += earnings

				with open("data/mainbank.json",'w') as f:
					json.dump(users,f)
				return
			else:
				await ctx.send(f"You lost the number was {str(number)}")
		if choice.content.lower() == "low":
			if number > hint:
				users = await get_bank_data()

				earnings = random.randrange(101)

				await ctx.send(f"You guessed right and earned {earnings}\nthe number was {str(number)}")


				users[str(user.id)]["wallet"] += earnings

				with open("data/mainbank.json",'w') as f:
					json.dump(users,f)
				return
			else:
				await ctx.send(f"You lost the number was {str(number)}")
		if choice.content.lower() == "same":
			if hint == number:
				users = await get_bank_data()

				earnings = random.randrange(101)

				await ctx.send(f"You guessed right and earned {earnings}\nthe number was {str(number)}")


				users[str(user.id)]["wallet"] += earnings

				with open("data/mainbank.json",'w') as f:
					json.dump(users,f)
				return
			else:
				await ctx.send(f"You lost the number was {str(number)}")
	@commands.command(aliases=["se"])
	async def snakeeyes(self,ctx,bet):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		bet = int(bet)
		dice1 = random.randrange(0,7)
		dice2 = random.randrange(0,7)
		if dice2 == 1 or dice1 == 1:
			user = ctx.author
			users = await get_bank_data()

			earnings = 1.8*bet

			embed = (discord.Embed(title = "Cerebrus Snakeyes",description = f"{dice1} | {dice2}\nyou won {earnings}",color = discord.Color.green()))
			await ctx.send(embed=embed)

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
		if dice1 == 1 and dice2 == 1:
			user = ctx.author
			users = await get_bank_data()

			earnings = 3*bet
			embed = (discord.Embed(title = "Cerebrus Snakeyes",description = f"{dice1} | {dice2}\nyou won {earnings}",color = discord.Color.green()))
			await ctx.send(embed=embed)

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
		if dice1 != 1 and dice2 != 1:
			user = ctx.author
			users = await get_bank_data()

			earnings = bet

			embed = (discord.Embed(title = "Cerebrus Snakeyes",description = f"{dice1} | {dice2}\nyou lost {earnings}",color = discord.Color.red()))
			await ctx.send(embed=embed)

			users[str(user.id)]["wallet"] += -1*earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)
		if dice1 == 1 and dice2 == 1:
			user = ctx.author
			users = await get_bank_data()

			earnings = bet
			embed = (discord.Embed(title = "Cerebrus Snakeyes",description = f"{dice1} | {dice2}\nyou won {earnings}",color=discord.Color.green()))
			await ctx.send(embed=embed)

			users[str(user.id)]["wallet"] += -1*earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)

	@commands.command(name="blockeco")
	async def blockeco(self,ctx,id):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		try:
			f = open("data/blockedusers.dat")
			f.close()
    # Do something with the file
		except FileNotFoundError:
			blockd = await ctx.send("Creating blocked data")
			pickle.dump(blockedusers,open("data/blockedusers.dat", "wb"))
			pickle.dump(bl,open("data/blockedusers.dat", "wb"))
			await asyncio.sleep(1)
			await blockd.edit("Created blocked data")
		id = int(id)
		if id != int:
			await ctx.send("Ids only, no mentions")
		blockuser(id)
		await ctx.send(f"succesfully blocked <@{id}> from economy")

	@commands.command(aliases=['bal'])
	async def balance(self, ctx,member:discord.Member=None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		for item in bl:
			if item == ctx.author.id:
				await ctx.send("You are blocked")
				return
		if member != None:
			await open_account(member)
			user = member
			users = await get_bank_data()
			wallet_amt = users[str(user.id)]["wallet"]
			bank_amt = users[str(user.id)]["bank"]
			fnet = wallet_amt+bank_amt
			wallet_amt = "{:,}".format(wallet_amt)
			bank_amt = "{:,}".format(bank_amt)
			fnet = "{:,}".format(fnet)
			em = discord.Embed(title=f"{member.name}'s Balance", description = f'**Wallet:** {wallet_amt}\n**Bank:** {bank_amt}\n**Net Worth:** {fnet}', color = discord.Color.magenta())
			em.set_footer(text = 'Eh')
			await ctx.send(embed= em)
			return
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()
		wallet_amt = users[str(user.id)]["wallet"]
		bank_amt = users[str(user.id)]["bank"]
		fnet = wallet_amt+bank_amt
		wallet_amt = "{:,}".format(wallet_amt)
		bank_amt = "{:,}".format(bank_amt)
		fnet = "{:,}".format(fnet)
		em = discord.Embed(title=f"{ctx.author.name}'s Balance", description = f'**Wallet:** {wallet_amt}\n**Bank:** {bank_amt}\n**Net Worth:** {fnet}', color = discord.Color.magenta())
		em.set_footer(text = 'Eh')
		await ctx.send(embed= em)
		return


	@commands.command()
	@commands.cooldown(1, 1440, commands.BucketType.user)
	async def daily(self, ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		user = ctx.author
		users = await get_bank_data()

		earnings = 1000

		await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

		users[str(user.id)]["wallet"] += earnings

		with open("data/mainbank.json",'w') as f:
			json.dump(users,f)
	@commands.command()
	@commands.cooldown(1, 10080, commands.BucketType.user)
	async def weekly(self, ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		user = ctx.author
		users = await get_bank_data()

		earnings = 10000

		await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

		users[str(user.id)]["wallet"] += earnings

		with open("data/mainbank.json",'w') as f:
			json.dump(users,f)
	@commands.command()
	@commands.cooldown(1, 43800, commands.BucketType.user)
	async def monthly(self, ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		user = ctx.author
		users = await get_bank_data()

		earnings = 30000

		await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

		users[str(user.id)]["wallet"] += earnings

		with open("data/mainbank.json",'w') as f:
			json.dump(users,f)
	
	@commands.command(name = 'blackjack', aliases = ['bj'])
	async def blackjack(self,ctx,amount):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		bal = await update_bank(ctx.author)
		amount = int(amount)
		if amount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return
		if amount < 100:
			await ctx.send("Bet must be at least **100**")
			return
		total_value = 0
		neocard1 = 0
		neocard2 = 0
		user = ctx.author
		users = await get_bank_data()
		card1 = random.randrange(1,11)
		card2 = random.randrange(1,11)
		ai1 = random.randrange(1,11)
		ai2 = random.randrange(1,11)
		if card1 == 11:
			ace = random.randint(0,1,10,11)
			card1 = ace
		if card2 == 11:
			ace = random.randint(0,1,10,11)
			card1 = ace
		total_value = card1 + card2
		aitotal = ai1 + ai2
		await self.try4bj(ctx,total_value,aitotal,amount,card1,card2)
		'''
		if try4bj.cont == True:
			await self.try4bj(ctx,hit.total_value,amount,card1,card2,hit.neocard)
			if self.try4bj.cont == True:
				await self.try4bj(ctx,hit.total_value,amount,card1,card2,hit.neocard,self.try4bj.neocard1)
				if self.try4bj.cont == True:
					embed = (discord.Embed(title="Cerebrus Casino",description = f"{card1} | {card2} | {hit.neocard} |{self.try4bj.neocard1} | {self.try4bj.neocard2}"))
					await ctx.send(embed=embed)

		if self.try4bj.cont == False:
			await ctx.send("game ended")
		'''

	
	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def beg(self, ctx):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		user = ctx.author
		if ctx.author.id == 746904488396324864:
			users = await get_bank_data()

			earnings = 999

			await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)

		else:


			users = await get_bank_data()

			earnings = random.randrange(101)

			await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

			users[str(user.id)]["wallet"] += earnings

			with open("data/mainbank.json",'w') as f:
				json.dump(users,f)


	@commands.command(aliases=['with'])
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def withdraw(self, ctx,amount = None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		if amount == None:
			await ctx.send("Please enter the amount")
			return

		bal = await update_bank(ctx.author)
		if amount == "all":
			amount = bal[1]
		amount = int(amount)

		if amount > bal[1]:
			await ctx.send('You do not have sufficient b alance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return

		await update_bank(ctx.author,amount)
		await update_bank(ctx.author,-1*amount,'bank')
		await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


	@commands.command(aliases=['dep'])
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def deposit(self, ctx,amount = None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		if amount == None:
			await ctx.send("Please enter the amount")
			return

		bal = await update_bank(ctx.author)
		if amount == "all":
			amount = bal[0]
		amount = int(amount)

		if amount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return

		await update_bank(ctx.author,-1*amount)
		await update_bank(ctx.author,amount,'bank')
		await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')

	@commands.command(aliases=["cf"])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def coinflip(self,ctx,amount=None,htc=None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		flip = "none"
		bal = await update_bank(ctx.author)
		intamount = 0.5*int(amount)
		origamount = int(amount)
		if origamount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if origamount < 0:
			await ctx.send('Amount must be positive!')
			return
		if origamount < 100:
			await ctx.send("Bet must be at least **100**")
			return
		if amount == None:
			await ctx.send("please enter an amount")
		intamount = 0.5*(intamount)
		if htc == None:
			await ctx.send("please enter heads or tails")
		ht =  random.randrange(1,3)
		if ht == 0:
			flip = "heads"
		if ht == 1:
			flip = "tails"
		if htc == flip:
			embed = (discord.Embed(title = "Cerebrus Casino",description="You won **" + amount + f"**\n your coin was {flip} :coin:",color=discord.Color.green()))
			await ctx.send(embed=embed)
			await update_bank(ctx.author,1*origamount)
		if htc != flip:
			amount = str(amount)
			embed = (discord.Embed(title = "Cerebrus Casino",description="You lost **" + amount + f"**\n the coin was {flip} :coin:",color=discord.Color.red()))
			await ctx.send(embed=embed)
			amount = int(amount)
			await update_bank(ctx.author,-1*origamount)


	@commands.command()
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def share(self, ctx,member : discord.Member,amount = None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		await open_account(member)
		if amount == None:
			await ctx.send("Please enter the amount")
			return

		bal = await update_bank(ctx.author)
		if amount == 'all':
			amount = bal[0]

		amount = int(amount)

		if amount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return

		await update_bank(ctx.author,-1*amount,'wallet')
		await update_bank(member,amount,'wallet')
		await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')
		await member.send(f"{ctx.author.name} gave you {amount}")
	@commands.command()
	async def reset(self,ctx):
		await ctx.send("reset")
	@commands.command()
	async def gift(self,ctx,member:discord.Member=None,item=None,amount=None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		if member == None:
			await ctx.send("`_gift @member item amount` eg. `_gift @kaneki#9586 watch 1`")
		if item == None:
			await ctx.send("`_gift @member item amount` eg. `_gift @kaneki#9586 watch 1`")
		if amount == None:
			await ctx.send("`_gift @member item amount` eg. `_gift @kaneki#9586 watch 1`")
		res = await check(ctx.author,item,1)

		if not res[0]:
			if res[1]==1:
				await ctx.send("That Object isn't there!")
				return
			if res[1]==2:
				await ctx.send(f"You don't have {item} in your bag.")
				return
			if res[1]==3:
				await ctx.send(f"You don't have {item} in your bag.")
				return

		sell_this(ctx.author,item,amount)
		buy_this(member,item,amount)

			
	@commands.command(aliases=['bankrob'])
	@commands.cooldown(1, 40, commands.BucketType.user)
	async def heist(self,ctx,user:discord.Member):
		userz = "nada"
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		pkg = "heist"
		check = await checkpkg(ctx.guild.id,pkg)
		role = discord.utils.find(lambda r: r.name == 'Heist Starter', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'heist starter', ctx.message.guild.roles)
		if role in ctx.author.roles or role2 in ctx.author.roles:
			check = "enabled"
		if check == "enabled":
			print("[Heist]: Enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall, to run heist while disabled for everyone else, make a role called `heist starter`")
			return
		lolz = await get_bank_data()
		await open_account(ctx.author)
		await open_account(user)
		dm = "t"
		bal = await update_bank(user)
		if bal[1]<10000:
			await ctx.send('It is useless to heist him :(')
			return
		heist_m = bal[1]
		embed = discord.Embed(title="Heist time",description = f"You will be heisting {user.name} for **{heist_m}**\nreact to join the heist\n*React with a thumbsup to DM results or Thumbsdown for Sending the results*",color=user.color)
		msg = await ctx.reply(embed=embed)
		await msg.add_reaction("👍")
		await msg.add_reaction("👎")
		def check(reaction, user):
			return userz == ctx.author
		reaction, userz = await self.bot.wait_for('reaction_add', check=check)
		if str(reaction) == ":thumbsup:":
			dm = "t"
			await msg.add_reaction("🎉")
			await ctx.reply("Dm enabled")
		elif str(reaction) == ":thumbsdown:":
			dm = "f"
			await msg.add_reaction("🎉")
			await ctx.reply("Dm disabled")
		await asyncio.sleep(20)
		new_msg = await ctx.channel.fetch_message(msg.id)

		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))
		gim = int(heist_m) / len(users)
		for item in users:
			await open_account(item)
			choice = ["win","win","win","fail","fail2"]
			choice = random.choice(choice)
			if item.id == user.id:
				await item.send("You can't join your own heist")
				choice = "nada"
			if choice == "win":
				if dm == "f":
					await ctx.send(f"{item.name} successfully heisted {user.name} and got {gim}")
				else:
					await item.send(f"You successfully heisted {user.name} and got {gim}")
				
				lolz[str(user.id)]["wallet"] -= gim
				lolz[str(item.id)]["wallet"] += gim

				with open("data/mainbank.json",'w') as f:
					json.dump(lolz,f)
			if choice == "fail" or choice == "fail2":
				lostm = random.randint(0,int(gim))
				if dm == "f":
					await ctx.send(f"{item.name} unsuccessfully heisted {user.name} and lost {lostm}")
				else:
					await item.send(f"You unsuccessfully heisted {user.name} and lost {lostm}")
				lolz = await get_bank_data()
				if choice == "fail2":
					lolz[str(user.id)]["wallet"] += lostm
					if dm == "f":
						await ctx.send(f"{item.name} tried to heist {user.name} and paid {user.name} {lostm}")
						await ctx.send(f"{item.name} unsuccessfully heisted {user.name} and lost {lostm}")
					else:
						await user.send(f"{item.name} tried to heist {user.name} and paid you {lostm}")
						await item.send(f"You unsuccessfully heisted {user.name} and lost {lostm}")
				lolz[str(item.id)]["wallet"] -= lostm

				with open("data/mainbank.json",'w') as f:
					json.dump(lolz,f)
		await ctx.send("Heist over")






	@commands.command(aliases=['rb'])
	@commands.cooldown(1, 40, commands.BucketType.user)
	async def rob(self, ctx,member : discord.Member):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		role = discord.utils.find(lambda r: r.name == 'Rob Starter', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'rob starter', ctx.message.guild.roles)
		pkg = "rob"
		check = await checkpkg(ctx.guild.id,pkg)
		if role in ctx.author.roles or role2 in ctx.author.roles:
			check = "enabled"
		if check == "enabled":
			print("[rob]: Enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall, to run rob while disabled for everyone else, make a role called `rob starter`")
			return
		await open_account(ctx.author)
		await open_account(member)
		bal = await update_bank(member)


		if bal[0]<100:
			await ctx.send('It is useless to rob him :(')
			return

		earning = random.randrange(0,bal[0])

		await update_bank(ctx.author,earning)
		await update_bank(member,-1*earning)
		await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def slots(self, ctx,amount = None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		if amount == None:
			await ctx.send("Please enter the amount")
			return

		bal = await update_bank(ctx.author)

		amount = int(amount)

		if amount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return
		if amount < 100:
			await ctx.send("Slots must be at least **100**")
			return
		final = []
		for i in range(3):
			a = random.choice(['❎','🅾','👑','🅰','🔑','🥈'])
			final.append(a)

		final = " | ".join(final)
		embed = (discord.Embed(title = "Cerebrus Casino",description = "Slots:\n" + str(final),color = discord.Color.green()))
		await ctx.send(embed=embed)

		if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
			await update_bank(ctx.author,2*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			embed = (discord.Embed(title = "Cerebrus Casino",description = "You won **" + str(amount) + "** Your current balance is **" + str(wallet_amt) + "**", color= discord.Color.green()))
			await ctx.send(embed=embed)
		else:
			await update_bank(ctx.author,-1*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			embed = (discord.Embed(title = "Cerebrus Casino",description = "You lost " + str(amount) + " Your current balance is " + str(wallet_amt), color= discord.Color.green()))
			await ctx.send(embed=embed)

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bet(self, ctx, amount = None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		if amount == None:
			await ctx.send("Please enter the amount")
		bal = await update_bank(ctx.author)

		amount = int(amount)

		if amount > bal[0]:
			await ctx.send('You do not have sufficient balance')
			return
		if amount < 0:
			await ctx.send('Amount must be positive!')
			return
		if amount < 100:
			await ctx.send("Bet must be at least **100**")
			return
		betrig = random.randrange(1,13)
		if betrig < 6:
			await update_bank(ctx.author,-1*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			boldwallet_amt = "**" + str(wallet_amt) + "**"
			embed = (discord.Embed(title = "Cerebrus Casino", description = "You rolled **" + str(betrig) + "**\nYou lost **" + str(amount) + "** Your current balance is " + boldwallet_amt, color = discord.Color.red() ))
			await ctx.send(embed=embed)
		if betrig > 6 and betrig < 8:
			await update_bank(ctx.author,0.5*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			boldwallet_amt = "**" + str(wallet_amt) + "**"
			wonhalf = 0.5*amount
			embed = (discord.Embed(title = "Cerebrus Casino", description = "You rolled " + str(betrig) + "**\nYou won **" + str(wonhalf) + "** Your current balance is " + boldwallet_amt, color = discord.Color.green() ))
			await ctx.send(embed=embed)
		if betrig > 8 and betrig < 11:
			await update_bank(ctx.author,2*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			boldwallet_amt = "**" + str(wallet_amt) + "**"
			embed = (discord.Embed(title = "Cerebrus Casino", description = "You rolled " + str(betrig) + "**\nYou won **" + str(amount) + "** Your current balance is " + boldwallet_amt, color = discord.Color.green() ))
			await ctx.send(embed=embed)
		if betrig == 12:
			await update_bank(ctx.author, 3*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			wonbet12 = amount*3
			boldwallet_amt = "**" + str(wallet_amt) + "**"
			embed = (discord.Embed(title = "Cerebrus Casino", description = "You rolled " + str(betrig) + "**\nYou won **" + str(wonbet12) + "** Your current balance is " + boldwallet_amt, color = discord.Color.green() ))
			await ctx.send(embed=embed)
		
	@commands.command()
	async def shop(self, ctx,*,args=None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		if args != None:
			if args == "watch" or args == "Watch":
				embed = (discord.Embed(title="A watch",description = "A somewhat useful device fo telling the time lol", color = discord.Color.green()))
				await ctx.send(embed=embed)
			#await ctx.send("WIP")
			return
		em = discord.Embed(title = "Shop",color = discord.Color.green())

		for item in mainshop:
			name = item["name"]
			price = item["price"]
			desc = item["description"]
			em.add_field(name = name, value = f"${price} | {desc}", inline = False)

		await ctx.send(embed = em)



	@commands.command()
	async def buy(self, ctx,item,amount = 1):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)

		res = await buy_this(ctx.author,item,amount)

		if not res[0]:
			if res[1]==1:
				await ctx.send("That Object isn't there!")
				return
			if res[1]==2:
				await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
				return


		await ctx.send(f"You just bought {amount} {item}")


	@commands.command(aliases=["inv"])
	async def bag(self, ctx,member:discord.Member=None):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		try:
			bag = users[str(user.id)]["bag"]
		except:
			bag = []


		em = discord.Embed(title = "Bag")
		for item in bag:
			name = item["item"]
			amount = item["amount"]
			em.add_field(name = name, value = amount, inline = False)
		await ctx.send(embed = em)

	@commands.command()
	async def sell(self, ctx,item):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		await open_account(ctx.author)
		amount = 1
		bolditem = "**" + item + "**"
		res = await sell_this(ctx.author,item,amount)

		if not res[0]:
			if res[1]==1:
				await ctx.send("That Object isn't there!")
				return
			if res[1]==2:
				await ctx.send(f"You don't have {amount} {item} in your bag.")
				return
			if res[1]==3:
				await ctx.send(f"You don't have {item} in your bag.")
				return
		if item == "watch":
			amount = 500
			boldamount = "**" + str(amount) + "**"
			await update_bank(ctx.author,1*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]["wallet"]
			boldwallet_amt = "**" + str(wallet_amt) + "**"
			embed = (discord.Embed(title = "Sold",description = "You sold " + bolditem + " for " + boldamount + "\n Your current balance is " + boldwallet_amt))
		await ctx.send(embed = embed)


	@commands.command(aliases = ["lb"])
	async def leaderboard(self, ctx,x = 5):
		await resetcd(ctx,ctx.author.id,ctx.author.name)
		users = await get_bank_data()
		leader_board = {}
		total = []
		for user in users:
			name = int(user)
			total_amount = users[user]["wallet"] + users[user]["bank"]
			leader_board[total_amount] = name
			total.append(total_amount)

		total = sorted(total,reverse=True)    

		em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
		index = 1
		for amt in total:
			id_ = leader_board[amt]
			member = self.bot.get_user(id_)
			name = member.name
			em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
			if index == x:
				break
			else:
				index += 1

		await ctx.send(embed = em)
	@commands.command()
	async def use(self,ctx,*,item,action=None):
		amount = 1
		if item == "xyz":
			res = await sell_this(ctx.author,item,amount)
			return
		if item == "ww" or "world walker":
			item = "worldwalker"
		if item == "ice" or "lebi":
			item = "lebi's_ice"
		res = await check(ctx.author,item,amount)
		if not res[0]:
			if res[1]==1:
				await ctx.send("That Object isn't there!")
				return
			if res[1]==2:
				await ctx.send(f"You don't have {item} in your bag.")
				return
			if res[1]==3:
				await ctx.send(f"You don't have {item} in your bag.")
				return
		if item == "watch":
			now = datetime.now()

			current_time = now.strftime("%H:%M:%S")
			embed = (discord.Embed(title = "Time ~ CS",description = "The time is " +  current_time ))
			await ctx.send(embed=embed)
			return
		elif item == "ice" or item == "lebi" or item == "lebi's_ice":
			await ctx.reply("You smoked some premnium ice and died in a hole with a rando")
			return


async def sell_this(user,item_name,amount,price = None):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			if price==None:
				price = 0.7* item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	users = await get_bank_data()

	bal = await update_bank(user)


	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt - amount
				if new_amt < 0:
					return [False,2]
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index+=1 
		if t == None:
			return [False,3]
	except:
		return [False,3]    

	with open("data/mainbank.json","w") as f:
		json.dump(users,f)

	await update_bank(user,cost,"wallet")

	return [True,"Worked"]

async def check(user,item_name,amount = None ,price = None):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			if price==None:
				price = 0.7* item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	users = await get_bank_data()

	bal = await update_bank(user)


	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt - amount
				if new_amt < 0:
					return [False,2]
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			#index+=1 
		if t == None:
			return [False,3]
	except:
		return [False,3]    

	#with open("data/mainbank.json","w") as f:
		#json.dump(users,f)

	#await update_bank(user,cost,"wallet")

	return [True,"Worked"]


async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open('data/mainbank.json','w') as f:
		json.dump(users,f)

	return True


async def get_bank_data():
	with open('data/mainbank.json','r') as f:
		users = json.load(f)

	return users


async def update_bank(user,change=0,mode = 'wallet'):
	users = await get_bank_data()

	users[str(user.id)][mode] += change

	with open('data/mainbank.json','w') as f:
		json.dump(users,f)
	bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
	return bal

async def buy_this(user,item_name,amount):
	item_name = item_name.lower()
	name_ = None
	for item in mainshop:
		name = item["name"].lower()
		if name == item_name:
			name_ = name
			price = item["price"]
			break

	if name_ == None:
		return [False,1]

	cost = price*amount

	users = await get_bank_data()

	bal = await update_bank(user)

	if bal[0]<cost:
		return [False,2]


	try:
		index = 0
		t = None
		for thing in users[str(user.id)]["bag"]:
			n = thing["item"]
			if n == item_name:
				old_amt = thing["amount"]
				new_amt = old_amt + amount
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t = 1
				break
			index+=1 
		if t == None:
			obj = {"item":item_name , "amount" : amount}
			users[str(user.id)]["bag"].append(obj)
	except:
		obj = {"item":item_name , "amount" : amount}
		users[str(user.id)]["bag"] = [obj]        

	with open("data/mainbank.json","w") as f:
		json.dump(users,f)

	await update_bank(user,cost*-1,"wallet")

	return [True,"Worked"]
		


def setup(bot):
    bot.add_cog(economy(bot))  