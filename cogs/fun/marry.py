import discord
from discord.ext import commands
import json
import os, re, aiohttp
import asyncio
import random
from cogs.misc.modulus import checkpkg

class Marry(commands.Cog, name='Marry'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=["t"])
	async def tree(self,ctx,user:discord.Member=None):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None:
			await open_account(ctx.author)
			users = await mdata()
			id = str(ctx.author.id)
			partner = users[id]["partner"]
			child = users[id]["name"]
			child2 = users[id]["name2"]
			child3 = users[id]["name3"]
			child4 = users[id]["name4"]
			child5 = users[id]["name5"]
			sibling = users[id]["sibling"]
			sibling2 = users[id]["sibling2"]
			embed = (discord.Embed(title = f"{ctx.author.name}'s tree",description = f"**Partner:**\n<@{partner}>\n**Children:**\n{child}\n{child2}\n{child3}\n{child4}\n{child5}\n**Siblings:**\n{sibling}\n{sibling2}",color=ctx.author.color))
			await ctx.send(embed=embed)
			return
		await open_account(user)
		users = await mdata()
		id = str(user.id)
		partner = users[id]["partner"]
		child = users[id]["name"]
		child2 = users[id]["name2"]
		child3 = users[id]["name3"]
		child4 = users[id]["name4"]
		child5 = users[id]["name5"]
		sibling = users[id]["sibling"]
		sibling2 = users[id]["sibling2"]
		embed = (discord.Embed(title = f"{ctx.author.name}'s tree'",description = f"**Partner:**\n<@{partner}>\n**Children:**\n{child}\n{child2}\n{child3}\n{child4}\n{child5}\n**Siblings:**\n{sibling}\n{sibling2}"))
		await ctx.send(embed=embed)
		return
	@commands.command()
	async def marry(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(user)
		await open_account(ctx.author)
		users = await mdata()
		if user == ctx.author:
			await ctx.send("marry someone besides yourself")
			return
		if user.id == users[str(ctx.author.id)]["parent"]:
			await ctx.send("let's not marry parents")
			return
		if user.name == users[str(ctx.author.id)]["name"]:
			await ctx.send("let's not marry children")
			return
		if user.name == users[str(ctx.author.id)]["name2"]:
			await ctx.send("let's not marry children")
			return
		if user.name == users[str(ctx.author.id)]["name3"]:
			await ctx.send("let's not marry children")
			return
		if user.name == users[str(ctx.author.id)]["name4"]:
			await ctx.send("let's not marry children")
			return
		if user.name == users[str(ctx.author.id)]["name5"]:
			await ctx.send("let's not marry children")
			return
		if user.name == users[str(ctx.author.id)]["sibling"]:
			await ctx.send("let's not marry siblings")
			return
		if user.name == users[str(ctx.author.id)]["sibling2"]:
			await ctx.send("let's not marry siblings")
			return
		if users[str(ctx.author.id)]["partner"] != "null" or users[str(user.id)]["partner"] != "null":
			await ctx.send("one of you is already married")
			return
		embed = discord.Embed(title="proposal time!",description = f"{ctx.author.name} has proposed to {user.name} :ring:\ntype `yes` or `no`",color = ctx.author.color)
		await ctx.send(embed=embed)
		try:
				choice = await self.bot.wait_for("message", check = lambda msg: msg.author == user, timeout = 30)
				if choice.content.startswith("yes"):				
					embed = discord.Embed(title = "wedding time!",description= f"{ctx.author.name} and {user.name} are now married",color = user.color)
					await ctx.send(embed=embed)
					users[str(ctx.author.id)]["partner"] = str(user.id)
					users[str(user.id)]["partner"] = str(ctx.author.id)
					with open('data/married/married.json','w') as f:
						json.dump(users,f)		
					return
				if choice.content.startswith("no"):
					await ctx.send("better luck next time")
					return
		except asyncio.TimeoutError:
			await user.send(f"{ctx.author.name} tried to marry you\ndue to timeout the marriage failed")
			await ctx.send("guess no wedding today...")
			return
	@commands.command()
	async def partner(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		users = await mdata()
		partner = users[str(ctx.author.id)]["partner"]
		if partner == "null":
			await ctx.send("marry someone first")
			return
		embed = discord.Embed(title = f"{ctx.author.name}'s partner",description = f"Your partner is <@{partner}>",color = ctx.author.color)
		await ctx.send(embed=embed)

	@commands.command()
	async def parent(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		users = await mdata()
		parent = users[str(ctx.author.id)]["parent"]
		if parent == "null":
			await ctx.send("find a dad/mom first")
			return
		embed = discord.Embed(title = f"{ctx.author.name}'s partner",description = f"Your parent is <@{parent}>",color = ctx.author.color)
		await ctx.send(embed=embed)
	@commands.command()
	async def makeparent(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		await open_account(user)
		users = await mdata()
		embed = discord.Embed(title="parent time!",description = f"{ctx.author.name} wants to become {user.name}'s parent :newspaper:\ntype `yes` or `no`",color = ctx.author.color)
		await ctx.send(embed=embed)
		try:
			choice = await self.bot.wait_for("message", check = lambda msg: msg.author == user, timeout = 30)
			if choice.content.startswith("yes"):
				print("continue")
			else:
				await ctx.send("maybe next time then...")
				return
		except asyncio.TimeoutError:
			await ctx.send("Guess no brother/sister today...")
			await user.send(f"{ctx.author.name} tried to make you their brother/sister")
		if users[str(ctx.author.id)]["parent"] != "null":
			await ctx.send("disown the current one dude...")
			return
		else:
			users[str(ctx.author.id)]["parent"] = str(user.id)
			await ctx.send("You have a parent now")
			with open("data/married/married.json","w") as f:
				json.dump(users,f)
	@commands.command()
	async def children(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		users = await mdata()
		child = users[str(ctx.author.id)]["name"]
		child2 = users[str(ctx.author.id)]["name2"]
		child3 = users[str(ctx.author.id)]["name3"]
		child4 = users[str(ctx.author.id)]["name4"]
		child5 = users[str(ctx.author.id)]["name5"]
		amount = users[str(ctx.author.id)]["amount"]
		if amount == "null":
			await ctx.send("marry someone first")
			return
		embed = discord.Embed(title = f"{ctx.author.name}'s children",description = f"Your children are:\n{child}\n{child2}\n{child3}\n{child4}\n{child5}\n*You have {amount} children*",color = ctx.author.color)
		await ctx.send(embed=embed)
	@commands.command()
	async def siblings(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		users = await mdata()
		child = users[str(ctx.author.id)]["sibling"]
		child2 = users[str(ctx.author.id)]["sibling2"]
		embed = discord.Embed(title = f"{ctx.author.name}'s siblings",description = f"Your siblings are:\n{child}\n{child2}",color = ctx.author.color)
		await ctx.send(embed=embed)
	@commands.command()
	async def mstart(self,ctx):
		await open_account(ctx.author)
		await ctx.send("started")
		print("started")
	@commands.command()
	async def divorce(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		users = await mdata()
		partner = users[str(ctx.author.id)]["partner"]
		if partner == "null":
			await ctx.send("marry someone first")
			return
		embed = discord.Embed(title = "Divorce",description = f"You successfully divorced <@{partner}>")
		user = ctx.guild.get_member(partner)
		await ctx.send(embed=embed)
		with open('data/married/married.json','w') as f:
			users[partner]["partner"] = "null"
			users[str(ctx.author.id)]["partner"] = "null"
			json.dump(users,f)
		await user.send(f"{ctx.author.name} divorced you")
	@commands.command()
	async def desibling(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		await open_account(user)
		users = await mdata()
		if users[str(ctx.author.id)]["sibling"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["sibling"] = "null"
				json.dump(users,f)
				await ctx.send("Bye Bye browther")
				return
		if users[str(ctx.author.id)]["sibling2"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["sibling2"] = "null"
				json.dump(users,f)
				await ctx.send("Bye Bye shishter")
				return
		else:
			await ctx.send("sibling not found")
	@commands.command()
	async def sibling(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		await open_account(user)
		users = await mdata()
		name = user.name
		embed = discord.Embed(title="sibling time!",description = f"{ctx.author.name} wants to become {user.name}'s sibling :newspaper:\ntype `yes` or `no`",color = ctx.author.color)
		await ctx.send(embed=embed)
		try:
			choice = await self.bot.wait_for("message", check = lambda msg: msg.author == user, timeout = 30)
			if choice.content.startswith("yes"):
				print("continue")
			else:
				await ctx.send("maybe next time then...")
				return
		except asyncio.TimeoutError:
			await ctx.send("Guess no brother/sister today...")
			await user.send(f"{ctx.author.name} tried to make you their brother/sister")
			return
		with open('data/married/married.json','w') as f:
			users[str(ctx.author.id)]["amount"] += 1
			if users[str(ctx.author.id)]["sibling"] == "null":
				users[str(ctx.author.id)]["sibling"] = name
				json.dump(users,f)
				return

			if users[str(ctx.author.id)]["sibling"] != "null":
				if users[str(ctx.author.id)]["sibling2"] == "null":
					users[str(ctx.author.id)]["sibling2"] = name
					json.dump(users,f)
					return					
				if users[str(ctx.author.id)]["sibling2"] != "null":
					await ctx.send("You can only have 2 siblings currently")
					return
	@commands.command()
	async def disown(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		await open_account(user)
		users = await mdata()
		users[str(user.id)]["parent"] = "null"
		users[str(ctx.author.id)]["amount"] -= 1
		if users[str(ctx.author.id)]["name"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["name"] = "null"
				json.dump(users,f)
				return
		if users[str(ctx.author.id)]["name2"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["name2"] = "null"
				json.dump(users,f)
				return
		if users[str(ctx.author.id)]["name3"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["name3"] = "null"
				json.dump(users,f)
				return
		if users[str(ctx.author.id)]["name4"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["name4"] = "null"
				json.dump(users,f)
				return
		if users[str(ctx.author.id)]["name5"] == user.name:
			with open('data/married/married.json','w') as f:
				users[str(ctx.author.id)]["name5"] = "null"
				json.dump(users,f)
				return
		
		if users[str(ctx.author.id)]["name"] != user.name or users[str(ctx.author.id)]["name2"] != user.name or users[str(ctx.author.id)]["name3"] != user.name or users[str(ctx.author.id)]["name4"] != user.name or users[str(ctx.author.id)]["name5"] != user.name:
			await ctx.send("Child not found")
			return
		else:
			embed = discord.Embed(title = "Hello Orphans...",description = f"{ctx.author.name} disowned {user.name}")
			await ctx.send(embed=embed)
			await user.send(f"{ctx.author.name} disowned you")
			return
	@commands.command()
	async def sex(self,ctx):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		name = None
		users = await mdata()
		chance = [1,2,3]
		chancer = random.choice(chance)
		if chancer == 3:
			await ctx.send(f"You go an STD and died lol, your stats have been reset {ctx.author.mention}")
			await mreset(ctx.author)
			return
		await ctx.send("You completed the act successfully :wink:\n type a name for your child")
		try:
			choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
			name = choice.content
			await ctx.send(f"Have fun with {name}")
		except asyncio.TimeoutError:
			await ctx.send("oh well good luck next time then...")
			return
		with open('data/married/married.json','w') as f:
			users[str(ctx.author.id)]["amount"] += 1
			if users[str(ctx.author.id)]["name"] == "null":
				users[str(ctx.author.id)]["name"] = name
				json.dump(users,f)
				return

			if users[str(ctx.author.id)]["name"] != "null":
				if users[str(ctx.author.id)]["name2"] == "null":
					users[str(ctx.author.id)]["name2"] = name
					json.dump(users,f)
					return					
				if users[str(ctx.author.id)]["name2"] != "null":
					if users[str(ctx.author.id)]["name3"] == "null":
						users[str(ctx.author.id)]["name3"] = name
						json.dump(users,f)
						return	
					if users[str(ctx.author.id)]["name3"] != "null":
						if users[str(ctx.author.id)]["name4"] == "null":
							users[str(ctx.author.id)]["name4"] = name
							json.dump(users,f)
							return	
						if users[str(ctx.author.id)]["name4"] != "null":
							if users[str(ctx.author.id)]["name5"] == "null":
								users[str(ctx.author.id)]["name5"] = name
								json.dump(users,f)
								return	
							if users[str(ctx.author.id)]["name5"] != "null":
								await ctx.send("5 children is the maximum for now")
								return
	@commands.command()
	async def adopt(self,ctx,user:discord.Member):
		pkg = "marry"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await open_account(ctx.author)
		await open_account(user)
		users = await mdata()
		embed = discord.Embed(title="adoption time!",description = f"{ctx.author.name} wants to adopt {user.name} :newspaper:\ntype `yes` or `no`",color = ctx.author.color)
		await ctx.send(embed=embed)
		try:
				choice = await self.bot.wait_for("message", check = lambda msg: msg.author == user, timeout = 30)
				if choice.content.startswith("yes"):
					print("continue")
				else:
					await ctx.send("maybe next time then...")
					return

		except asyncio.TimeoutError:
			await ctx.send("Guess no papers needed...")
			await user.send(f"{ctx.author.name} tried adopting you")
			return
		embed = discord.Embed(title="adoption time!",description = f"{ctx.author.name} welcome {user.name} to your family !",color = user.color)
		await ctx.send(embed=embed)		
		with open('data/married/married.json','w') as f:
			users[str(user.id)]["parent"] = str(ctx.author.id)
			users[str(ctx.author.id)]["amount"] += 1
			if users[str(ctx.author.id)]["name"] == "null":
				users[str(ctx.author.id)]["name"] = user.name
				json.dump(users,f)
				return

			if users[str(ctx.author.id)]["name"] != "null":
				if users[str(ctx.author.id)]["name2"] == "null":
					users[str(ctx.author.id)]["name2"] = user.name
					json.dump(users,f)
					return					
				if users[str(ctx.author.id)]["name2"] != "null":
					if users[str(ctx.author.id)]["name3"] == "null":
						users[str(ctx.author.id)]["name3"] = user.name
						json.dump(users,f)
						return	
					if users[str(ctx.author.id)]["name3"] != "null":
						if users[str(ctx.author.id)]["name4"] == "null":
							users[str(ctx.author.id)]["name4"] = user.name
							json.dump(users,f)
							return	
						if users[str(ctx.author.id)]["name4"] != "null":
							if users[str(ctx.author.id)]["name5"] == "null":
								users[str(ctx.author.id)]["name5"] = user.name
								json.dump(users,f)
								return	
							if users[str(ctx.author.id)]["name5"] != "null":
								await ctx.send("5 children is the maximum for now")
								return
						


			
			#await addchild(ctx.author,user,None,None)
			
async def mdata():
	with open('data/married/married.json','r') as f:
		users = json.load(f)

	return users
async def addchild(author,user,amount,status):
	users = await mdata()

	with open('data/married/married.json','w') as f:
		json.dump(users,f)
	
async def open_account(user):

	users = await mdata()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["partner"] = "null"
		users[str(user.id)]["amount"] = 0
		users[str(user.id)]["name"] = "null"
		users[str(user.id)]["name2"] = "null"
		users[str(user.id)]["name3"] = "null"
		users[str(user.id)]["name4"] = "null"
		users[str(user.id)]["name5"] = "null"
		users[str(user.id)]["status"] = "alive"
		users[str(user.id)]["parent"] = "null"
		users[str(user.id)]["sibling"] = "null"
		users[str(user.id)]["sibling2"] = "null"
		with open('data/married/married.json','w') as f:
			json.dump(users,f)

async def mreset(user):
		users = await mdata()
		users[str(user.id)]["partner"] = "null"
		users[str(user.id)]["amount"] = 0
		users[str(user.id)]["name"] = "null"
		users[str(user.id)]["name2"] = "null"
		users[str(user.id)]["name3"] = "null"
		users[str(user.id)]["name4"] = "null"
		users[str(user.id)]["name5"] = "null"
		users[str(user.id)]["status"] = "alive"
		users[str(user.id)]["parent"] = "null"
		users[str(user.id)]["sibling"] = "null"
		users[str(user.id)]["sibling2"] = "null"

		with open('data/married/married.json','w') as f:
			json.dump(users,f)

		return True




def setup(bot):
	bot.add_cog(Marry(bot))