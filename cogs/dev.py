import discord, random
from discord.ext import commands
import json
import os
import subprocess
import asyncio
from io import StringIO
import sys

with open("data/devs.json","r") as file:
	file = json.load(file)
	devs = file["devs"]

class developer(commands.Cog, name='Developer'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='core')
	async def core(self,ctx, action:str, input=None):
		if ctx.author.id not in devs:
			return await ctx.send('You are not authorized to perform this command.')
		with open("data/devs.json","r") as file:
			file = json.load(file)
		if action in "adddev":
			file["devs"].append(input) 
			with open("data/devs.json") as file2:
				json.dump(file,file2)
		elif action in "restart":
			await ctx.send('Restarting...')
			os.system("python restart.py")
		elif action in "shutdown":
			await ctx.send("Shutting Systems down...")
			await self.bot.close()
		elif action == "reload":
			input = input.split('/')
			try:
				main = await ctx.send('Beginning Reload...')
				self.bot.unload_extension(f'cogs.{input[0]}.{input[1]}')
				await main.edit(content=f'Unloaded Cog {input[1]}...')
				self.bot.load_extension(f"cogs.{input[0]}.{input[1]}")
				await main.edit(content='Reloaded Cog.')
			except FileNotFoundError:
				await ctx.send("Could not find file. Improper Path")
		elif action == "unload":
			input = input.split('/')
			try:
				main = await ctx.send('Beginning Unload...')
				self.bot.unload_extension(f'cogs.{input[0]}.{input[1]}')
				await main.edit(content=f'Unloaded Cog {input[1]}...')
			except FileNotFoundError:
				await ctx.send("Could not find file. Improper Path")
		elif action == "load":
			input = input.split('/')
			try:
				main = await ctx.send('Beginning Load...')
				self.bot.load_extension(f"cogs.{input[0]}.{input[1]}")
				await main.edit(content='Loaded Cog.')
			except FileNotFoundError:
				await ctx.send("Could not find file. Improper Path")

		elif action in "src" or action in "repl":
			await ctx.send('DMed to you!')
			embed = discord.Embed(title='Source Code, with IDE Invite', description = '[Repl Invite](https://replit.com/join/sespilaq-ace6002)\n[GitHub Source, need access to it](https://github.com/Project-Cerebrus/Project-Cerebrus)', color=discord.Color.green())
			await ctx.author.send(embed=embed)

		elif action in "status":
			if input.lower().startswith("playing"):
				input = input.replace("playing",'')
				activitytype = discord.Game(name=input)

			elif input.lower().startswith("streaming"):
				inputlist = input.split(' | ')
				activitytype = discord.Streaming(name=inputlist[0].replace('streaming',''), url = inputlist[1])
			elif input.lower().startswith("listening"):
				input = input.replace("listening",'')
				activitytype = discord.Activity(type=discord.ActivityType.listening, name=input)
			elif input.lower().startswith("watching"):
				input = input.replace("watching",'')
				activitytype = discord.Activity(type=discord.ActivityType.watching, name=input)
			else:
				print(input)
				return await ctx.send('Activity Type not Found')
			await self.bot.change_presence(status = discord.Status.do_not_disturb,activity=activitytype)
			await ctx.send('Changed!')

	
	@commands.command()
	async def eval(self,ctx,*,args):
		old_stdout = sys.stdout
		sys.stdout = mystdout = StringIO()

		eval(args)

		sys.stdout = old_stdout

		message = mystdout.getvalue()
		embed = (discord.Embed(title="**Cerebrus Shell**",description =f"**Output:**\n```\n{message}\n```",color=discord.Color.green()))
		await ctx.send(embed=embed)
	@commands.command(aliases=["some1","someone"])
	async def enryu(self,ctx):
		await ctx.send("hi i won't bully u ~ Cerebrus")
	@commands.command()
	async def ensh(self,ctx,*,args):
		old_stdout = sys.stdout
		sys.stdout = mystdout = StringIO()

		eval(args)

		sys.stdout = old_stdout

		message = mystdout.getvalue()
		await ctx.send(message)

	@commands.command()
	async def whoami(self,ctx):
		embed = (discord.Embed(title = 'Who am I?', description = 'I am Cerebus, Ruler of hell. Also a discord bot lol. type `_help` for all my commands or `_devs` for my developers info(`_bio` eg. `_bio kaneki`)', colour = discord.Color.green())
		.set_footer(text = 'The ruler of hell exits the stage...'))
		await ctx.send(embed=embed)

	@commands.command()
	async def vote(self, ctx):
		embed = (discord.Embed(title = 'Vote for Me!', description = 'Thanks for choosing me!\n**[Click Me](https://discordbotlist.com/bots/cerebrus)**\n\n', colour = discord.Color.green())
		.set_footer(text = 'Ty for choosing our bot <3 ~ Devs'))
		await ctx.send(embed=embed)
	@commands.command()
	async def invite(self, ctx):
		embed = (discord.Embed(title = 'Invite Me!', description = 'Thanks for choosing me!\n**[Click Me](https://discord.com/api/oauth2/authorize?client_id=829241822278058025&permissions=8&scope=bot%20applications.commands)**\n\n', colour = discord.Color.green())
		.set_footer(text = 'Ty for choosing our bot <3 ~ Devs'))
		await ctx.send(embed=embed)
	@commands.command()
	async def website(self, ctx):
		embed = (discord.Embed(title = 'Our website!', description = 'Thanks for choosing me!\n**[Click Me](https://cerebus.ace6002.repl.co/)**\n\n', colour = discord.Color.green())
		.set_footer(text = 'Ty for choosing our bot <3 ~ Devs'))
		await ctx.send(embed=embed)
	@commands.command(aliases = ['devs','dev'])
	async def credits(self, ctx):
		embed = discord.Embed(title = 'My Developers', description = 'They worked hard on me', colour = discord.Color.green())
		embed.add_field(name='1. Ace\'#9999', value = 'Lead Developer・45% Contribution', inline=False)
		embed.add_field(name='2. Kaneki#9876 ~ Eris the eshay', value='Lead Developer・45% Contribution', inline=False)
		embed.add_field(name='3. Skull Crusher#0003', value = 'Backend Developer・10% Contribution', inline=False)
		embed.set_footer(text='Don\'t send them a friend req')
		await ctx.send(embed=embed)

	@commands.command(aliases = ['server'])
	async def support(self, ctx):
		embed = (discord.Embed(title = 'Support Server!', description = 'Join for help\n\n**[Click Me](https://discord.gg/Q6cMuRGCXj)**\n\n', colour = discord.Color.green())
		.set_footer(text = 'Ty for choosing our bot <3 ~ Devs'))
		await ctx.send(embed=embed)
	
		
	@commands.command(name='ping', brief = 'Gives the latency', description = 'Gives the latency in milliseconds', aliases = ['latency'])
	async def ping(self, ctx):
		embed=discord.Embed(title = "My Current Latency Is", description = f"{round(self.bot.latency*1000)} ms", color = discord.Color.magenta())
		await ctx.send(embed=embed)

	@commands.command(name = "todo")
	async def todo(self, ctx):
		with open("todo.txt") as td:
			content = "\n".join(td.readlines())
		await ctx.send(content)
		print("sent")
		return

	@commands.command(name = "changelog",aliases=["chl"])
	async def changelog(self, ctx):
		with open("changelog.txt") as chl:
			content = "\n".join(chl.readlines())
		await ctx.send(content)
		print("sent")
		return

	@commands.command()
	async def restart(self, ctx,*,args=None):
		if ctx.author.id not in devs:
			return await ctx.send('You are not authorized to do this')
		await ctx.send('Restarting...')
		os.system("python restart.py")

	@commands.command()
	async def addtd(self, ctx,message, pwd, *,args):
		if pwd == "tododevslol":
			await ctx.message.delete()
			f = open("todo.txt", "a")
			f.write("\n" + "- " + args)
			f.close()
			await ctx.send("Successfully added")
			return
		else:
			await ctx.send("Password required...")
	@commands.command()
	async def deltd(self, ctx, *,args):
		await ctx.send("Make sure to type the text to be deleted eg. `-deltd update mutrole`")
		
		a_file = open("todo.txt", "r")

		lines = a_file.readlines()
		a_file.close()
		delstuff = "- " + args
		new_file = open("todo.txt", "w")
		for line in lines:
			if line.strip("\n") != delstuff:
				new_file.write(line)
		print("deleted")
		await ctx.send("successfully deleted")
		return

	@commands.command(name = "shlog")
	async def shlog(self, ctx):
		with open("log.txt") as x:
			content2 = "\n".join(x.readlines())
		await ctx.send(content2)
		return

	@commands.command(aliases= ["exec"], brief = "exec from terminal")
	async def sh(self, ctx, *,args):
		#os.system(args)
		outputsh = subprocess.check_output(args, shell=True)
		printoutputsh = "`" + args + "`"
		await ctx.send("successfully executed " + printoutputsh)
		autheval = str(ctx.author.id)
		f = open("log.txt", "a")
		f.write("\n" +  "<@" + autheval + ">" + " :" + args)
		f.close()
		await ctx.send(outputsh)
		return

# bio - prolly add db so for everypne
	@commands.command()
	async def bio(self,ctx,action,*,args=None):
		async def getbio():
			with open("data/bio.json","r")as f:
				users = json.load(f)
			return users
		async def openbio(id,biostuff):
			users = await getbio()
			check4bio = users[str(id)]["bio"]
			if str(id) in users and check4bio != "null":
				print("[BIO]: already there")
				return
			else:
				users[str(id)] = {}
				users[str(id)]["bio"] = args
				with open("data/bio.json","w") as f:
					json.dump(users,f)
		if action == "+" or action == "add":
			await openbio(ctx.author.id,args)
			await ctx.send("added bio")
			return
		elif action == "-" or action == "remove":
			users = await getbio()
			users[str(ctx.author.id)]["bio"] = "null"
			with open("data/bio.json","w") as f:
				json.dump(users,f)
			await ctx.send("removed bio")
			return
		else:
			users = await getbio()
			if args == None:
				try:
					test4bio = users[str(action)]["bio"]
				except KeyError:
					test4bio = "null"
				if test4bio == "null":
					await ctx.send("No bio args found, run as `bio add <bio>`")
					return
				else:
					pass
			if str(action) not in users:
				await ctx.send("User does not have a bio set or you haven't used their id, `bio add <bio>`")
			else:
				bio = users[str(action)]["bio"]
				await ctx.send(bio)
		





	@commands.command()
	async def devbio(self, ctx,*,args = None):

		if args == "kaneki" or args == "eris":
			w = await ctx.send("General kool kid, likes exploiting devices. What are you waiting for? DM him, lol. I liek programming... hru? This message will self destruct in **5**... :)")
			await asyncio.sleep(1)
			await w.edit(content="General kool kid, likes exploiting devices. What are you waiting for? DM him, lol. I liek programming... hru? This message will self destruct in **4**... :)")
			await asyncio.sleep(1)
			await w.edit(content="General kool kid, likes exploiting devices. What are you waiting for? DM him, lol. I liek programming... hru? This message will self destruct in **3**... :)")
			await asyncio.sleep(1)
			await w.edit(content="General kool kid, likes exploiting devices. What are you waiting for? DM him, lol. I liek programming... hru? This message will self destruct in **2**... :)")
			await asyncio.sleep(1)
			await w.edit(content="General kool kid, likes exploiting devices. What are you waiting for? DM him, lol. I liek programming... hru? This message will self destruct in **1**... :)")
			await asyncio.sleep(1)
			await w.delete()
			await ctx.send("destructed kaneki's bio lol")
			return


		if args == "lucky":
			await ctx.send("handsomely devilish 15 year old boy loved by both men *and* women")
			return

		if args == "help":
			await ctx.send("Bio is for ace and kaneki and skull eg. _bio ace")
			return
		if args == "sandy":
			await ctx.send("pieck is queen")
		if args == None:
			await ctx.send("`_bio help` for information about the bio command")
			return
		return

	@commands.command(name = "suggestions")
	async def suggestions(self, ctx):
		with open("suggestions.txt") as sg:
			content = "\n".join(sg.readlines())
		await ctx.send(content)
		print("sent")
		return


def setup(bot):
    bot.add_cog(developer(bot))