import discord, random, TenGiphPy, aiohttp, json, asyncio, platform, sys, os, requests, datetime, time, pyjokes, names, akinator
from discord.ext import commands
from typing import Optional
import urllib.request
from aiohttp import request
from cogs.misc.modulus import checkpkg
tokens = {'tenor': 'BDE8TTQAN0H1'}


class fun(commands.Cog, name='Fun'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(name='aki', aliases = ['akistart', 'akinator'])
	async def akinator(self, ctx):
		aki = akinator.Akinator()

		q = aki.start_game()

		embed = (discord.Embed(title="Akinator Game", description = "As the Embed edits and asks questions react with...\n<a:thumbsup:839805861324783626> for Yes\n<a:thumbsdown:839805861241028608> for No\n<a:pd_maybe:844104175280717835> for Probably\n<:thonkwoke:844104503170039828> for Probably Not\n<:IDK:844104911431008256> for I Don't Know\n<a:lefter_arrow:844116180541112330> for Back\n<:abc:844115854961672223> for Cancel", color = discord.Color.green())
		.add_field(name='Current Question', value=q))
		main=await ctx.send(embed=embed)
		await main.add_reaction("<a:thumbsup:839805861324783626>")
		await main.add_reaction("<a:pd_maybe:844104175280717835>")
		await main.add_reaction("<:thonkwoke:844104503170039828>")
		await main.add_reaction("<:IDK:844104911431008256>")
		await main.add_reaction("<a:thumbsdown:839805861241028608>")
		await main.add_reaction("<:abc:844115854961672223>")
		await main.add_reaction("<a:lefter_arrow:844116180541112330>")

		while aki.progression <= 80:
			embed = (discord.Embed(title="Akinator Game", description = "React with...\n<a:thumbsup:839805861324783626> for Yes\n<a:thumbsdown:839805861241028608> for No\n<a:pd_maybe:844104175280717835> for Probably\n<:thonkwoke:844104503170039828> for Probably Not\n<:IDK:844104911431008256> for I Don't Know\n<a:lefter_arrow:844116180541112330> for Back\n<:abc:844115854961672223> for Cancel", color = discord.Color.green())
			.add_field(name='Current Question', value=q)
			.set_footer(text=f"{ctx.author.name}'s Akinator Game", icon_url=ctx.author.avatar_url))
			await main.edit(embed=embed)
			def check(reaction, user):
				return user == ctx.author
			reaction, user = await self.bot.wait_for('reaction_add', check=check)
			await main.remove_reaction(reaction,user)
			if str(reaction) == "<:IDK:844104911431008256>":
				a = 'idk'
			elif str(reaction) == "<:thonkwoke:844104503170039828>":
				a = 'pn'
			elif str(reaction) == '<a:pd_maybe:844104175280717835>':
				a = 'p'
			elif str(reaction) == '<a:thumbsdown:839805861241028608>':
				a = 'no'
			elif str(reaction) == '<a:thumbsup:839805861324783626>':
				a = 'y'
			elif str(reaction) == "<a:lefter_arrow:844116180541112330>":
				a = 'back'
			elif str(reaction) == "<:abc:844115854961672223>":
				return await main.delete()
			else:
				pass
			if a == "back":
				try:
					q = aki.back()
				except akinator.CantGoBackAnyFurther:
					pass
			else:
				q = aki.answer(a)
		aki.win()

		embed = discord.Embed(title=f"It's {aki.first_guess['name']} ({aki.first_guess['description']})", description = 'Hope I was correct!', color=discord.Color.green())
		embed.set_image(url=aki.first_guess['absolute_picture_path'])

		await main.edit(embed=embed)
		await main.clear_reactions()

	@commands.command(aliases=["randomnick","randomname"])
	async def rnick(self,ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		nick = names.get_full_name()
		try:
			await ctx.author.edit(nick=nick)
			await ctx.send(f"We\'ll call you, {nick}")
		except:
			await ctx.send(f"We\'ll call you, {nick}\nCould not edit nickname, missing permissions")
	@commands.command()
	async def riddle(self,ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		with open("data/riddles.json","r") as f:
			users = json.load(f)
			numbers = [0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
          11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
          31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
          41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
          51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
          61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
          71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
          81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
          91, 92, 93, 94, 95, 96, 97, 98]
			no = random.choice(numbers)
			#no = str(no)
			question = users[no]["question"]
			answer = users[no]["answer"]
			embed = discord.Embed(title="Riddle Time!",description=f"Question: {question}\nAnswer: ||{answer}||",color=ctx.author.color)
			await ctx.send(embed=embed)
	@commands.command()
	async def trump(self,ctx):
		url = "https://matchilling-tronald-dump-v1.p.rapidapi.com/random/quote"

		headers = {
				'accept': "application/hal+json",
				'x-rapidapi-key': "a5b0325a1dmsh8e6bcbe244a2c36p1716e9jsn50d33c6c7737",
				'x-rapidapi-host': "matchilling-tronald-dump-v1.p.rapidapi.com"
				}

		response = requests.request("GET", url, headers=headers)

		print(response.text)
		response = response.json()
		qod = response["value"]
		embed = discord.Embed(title = "Tumpy m'boy",description=f"{qod}",color = discord.Color.orange())
		await ctx.send(embed=embed)
	@commands.command()
	async def joke(self,ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		joke = pyjokes.get_joke()
		embed = discord.Embed(title = "Joke Time!",description=joke,color= ctx.author.color)
		await ctx.send(embed=embed)
	@commands.command(aliases=["cf2"])
	async def coinflip2(self,ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		coin = ["heads","tails"]
		choice = random.choice(coin)
		embed = discord.Embed(title="Cerebrus CoinFlip",description = f"You got {choice} :coin:", color = discord.Color.green())
		await ctx.send(embed=embed)
	@commands.command()
	async def quote(self,ctx,*,msg):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await ctx.send(f"{msg}\n-**{ctx.author.name}**")
	@commands.command(aliases = ["hotchocolate","whoami2"])
	async def htc(self,ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await ctx.send("see im hot chocolate not rly the ruler of hell so drink up my pretties")
	@commands.command()
	async def urban(self,ctx, *msg):
		pkg = "inap"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		word = ' '.join(msg)
		api = "http://api.urbandictionary.com/v0/define"
		# Send request to the Urban Dictionary API and grab info
		response = requests.get(api, params=[("term", word)]).json()
		embed = discord.Embed(description="No results found!", colour=0xFF0000)
		if len(response["list"]) == 0:
				return await ctx.send(embed=embed)
		# Add results to the embed
		embed = discord.Embed(title="Word", description=word, colour=discord.Color.green())
		embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
		embed.add_field(name="Examples:", value=response['list'][0]['example'])
		await ctx.send(embed=embed)
		return

	@commands.command()
	async def ben(self,ctx,user:discord.Member):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		await ctx.message.delete()
		await ctx.send(f"Successfully banned **{user.name}**")
	@commands.command(aliases=["msg"])
	async def dm(self, ctx,member:discord.User,*,args):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		with open("data/blockedusers.json", "r") as f:
			blusers = json.load(f)
		#blockedusers = []
		# iterate through every user
		for user in blusers["user"]:
				# get the captchacode
				test4blockd = user["id"]
				# check if the code matches
				if test4blockd == ctx.author.id:
					await ctx.send("You have been blocked from using dm/msg")
					return
				else:
					await member.send("<@" + str(ctx.author.id) + "> : " + args)
					await ctx.send("Succesfully messaged `" + args + "` to " + member + ".")
					return
	@commands.command(name="fact")
	async def fact(self, ctx, animal: str):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = discord.Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")
	@commands.command()
	async def thesis(self,ctx,thesises=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if thesises == None:
			embed = (discord.Embed(title="Thesis",description="thesises avaliable:\nbra1n break ~ Kaneki\nDM a developer by doing `_devs` to add your thesis",color = discord.Color.green()))
			await ctx.send(embed=embed)
		if thesises == "bra1n break" or thesises == "bra1n" or thesises == "bra1nbreak":
			embed = (discord.Embed(title = "Bra1n break",description = "**thesis : could a hypnotist unlock 100% of the human brain?**\nA hypnotist is able to bypass average human barriers that would take a huge amount of time to gain iron will-power, this is because of a hypnotist being able to fully convince humans that they can do something.\n \nSo onto the main topic, theoritically if you had the following aquiring 100% of your brain with a hypnotist would be possible\n**Needed theories:**\n1. The fact that we know what will be needed to bypass the barrier\n2. the fact that the human brain won't 'crash' upon unlocking 100% of their brain\n3. The fact that we don't already have 100% unlocked\nNow, stats estimate the we have 15% or out brain to use and 85% is unused, let's say that to gain 100% access of your brain you need an iron will, a sort of compaitiblity with the hypnotist and have successfully been bypassed for less important human limits before. If the human brain can't take the strain of unlocking 100% in one go then start with 5% and 5%, let's say the stats are false so this is where common logic comes in, if we can even unlock 1% we can unlock more. So once we've successfully unlocked 100% of the brain in x amount of time, we need to find out what the changes are to develop a 'quick bypass' so that we can bypass the barrier fast and effectively. After we have developed a quick bypass, we have to decide who to give it to and who not to. It should start with 3 people of very high integrity , 3 is the minamal number to vote. In conclusion though the thesis is shaky it's certainly possible.",color = discord.Color.green()))
			await ctx.author.send(embed=embed)
			await ctx.send("check your DMs")

	@commands.command()
	async def rps(self,ctx,user:discord.Member,games=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		userchoice = "none"
		authorchoice = "none"
		await ctx.send("both users check your DMs")
		if games == None:
			games = 1 
		games = int(games)
		authcounter = 0
		opcounter = 0

		#while authcounter != games or opcounter != games:
		await ctx.author.send("`rock`,`paper` or `scissors`")
		await user.send("`rock`,`paper` or `scissors`")
		try:
			choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
			print(choice.content)
			if choice.content.lower() == "rock":
				userchoice = "rock"
			if choice.content.lower() == "paper":
				userchoice = "paper"
			if choice.content.lower() == "scissors":
				userchoice = "scissors"
		except asyncio.TimeoutError:
			await ctx.author.send("smh you didn't respond")
			await user.send("Your opponent didn't respond so you won")
		try:
			choice2 = await self.bot.wait_for("message", check = lambda msg: msg.author == user, timeout = 30)
			print(choice.content)
			if choice2.content.lower() == "rock":
				authorchoice = "rock"
			if choice2.content.lower() == "paper":
				authorchoice = "paper"
			if choice2.content.lower() == "scissors":
				authorchoice = "scissors"
		except asyncio.TimeoutError:
			await user.send("smh you didn't respond")
			await ctx.author.send("Your opponent didn't respond so you won")
		if userchoice == "rock":
			if authorchoice == "paper":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you lost")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you won")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{user.mention} won")
				opcounter += 1
				await asyncio.sleep(1)
			if authorchoice == "rock":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, tie")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, tie")
				await ctx.send(f"{ctx.author.mention},{user.mention}\nthis game was a tie")
				await asyncio.sleep(1)
			if authorchoice == "scissor":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you won")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you lost")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{ctx.author.mention} won")
				authcounter += 1
				await asyncio.sleep(1)
		if userchoice == "paper":
			if authorchoice == "scissor":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you lost")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you won")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{user.mention} won")
				opcounter += 1
				await asyncio.sleep(1)
			if authorchoice == "paper":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, tie")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, tie")
				await ctx.send(f"{ctx.author.mention},{user.mention}\nthis game was a tie")
				await asyncio.sleep(1)
			if authorchoice == "rock":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you won")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you lost")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{ctx.author.mention} won")
				authcounter += 1
				await asyncio.sleep(1)
		if userchoice == "scissor":
			if authorchoice == "rock":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you lost")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you won")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{user.mention} won")
				opcounter += 1
				await asyncio.sleep(1)
			if authorchoice == "scissor":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, tie")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, tie")
				await ctx.send(f"{ctx.author.mention},{user.mention}\nthis game was a tie")
				await asyncio.sleep(1)
			if authorchoice == "paper":
				await ctx.author.send(f"You did {authorchoice} and your opponent did {userchoice}, you won")
				await user.send(f"You did {userchoice} and your opponent did {authorchoice}, you lost")
				await ctx.send(f"{ctx.author.mention},{user.mention}\n{ctx.author.mention} won")
				authcounter += 1
				await asyncio.sleep(1)
		

	@commands.command(name='echo' , brief='Echoes a message', description='Echoes a message into a specified channel\nSyntax: //echo [channel] [message]', aliases = ['say'])
	async def echo(self, ctx, channel=None,  *, msg_echo=None):
		pkg = "echo"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if msg_echo is None:
			await ctx.reply('The syntax is `-echo #channel <msg>`')
			return
		if channel is None:
			await ctx.reply('The syntax is `-echo #channel <msg>`')
			return
		if str(channel).startswith('<#'):
			if '@everyone' in msg_echo or '@here' in msg_echo:
				await ctx.reply('Nice try but you cant ping using me.')
				return
			channelid = channel.replace('<#','')
			channelid = channelid.replace('>','')
			channel = ctx.guild.get_channel(int(channelid))
			await channel.send(str(msg_echo))
			await ctx.message.add_reaction('<a:pd_Tick:800827330292613140>')
		else:
			await ctx.reply('The syntax is `-echo #channel <msg>`')

	@commands.command(name='simprate', brief = 'Rates how simp you/someone is', description = 'Rates how simp you/someone is\nSyntax //simprate [person if you want to simprate someone]')
	async def simprate(self, ctx, *, torate:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		torate = ctx.author
		percent = random.randrange(0,100)
		if torate == None:
			torate = ctx.author.display_name
		elif torate.id == 802883472628121620:
			percent = 100
		
		gembed = discord.Embed(title = 'SimpRate Machine', description = f"{torate} is {percent}% Simp :blush:", colour = discord.Colour.magenta())
		await ctx.send(embed=gembed)

	@commands.command(name='kiss', aliases=['liplock'])
	async def kiss(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None or user == ctx.author:
			await ctx.reply('Sorry, i dont facilitate self-kissing.')
			return
		else:
			a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
			webhook = await ctx.channel.create_webhook(name = "UNamed")
			t = TenGiphPy.Tenor(token=tokens['tenor'])
			kiss_gif = await t.arandom("anime kiss")
			embed=discord.Embed(title = f"{ctx.author.name} kisses {user.name}", colour = discord.Colour.from_rgb(a,b,c)).set_image(url=kiss_gif)
			await webhook.send(content = user.mention, embed=embed , username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
			await webhook.delete()
	@commands.command(name='lick', aliases=['licklol'])
	async def lick(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None or user == ctx.author:
			await ctx.reply('Sorry, i dont facilitate self-licking.')
			return
		else:
			a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
			webhook = await ctx.channel.create_webhook(name = "UNamed")
			t = TenGiphPy.Tenor(token=tokens['tenor'])
			kiss_gif = await t.arandom("anime lick")
			embed=discord.Embed(title = f"{ctx.author.name} licks {user.name}", colour = discord.Colour.from_rgb(a,b,c)).set_image(url=kiss_gif)
			await webhook.send(content = user.mention, embed=embed , username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
			await webhook.delete()
	@commands.command(name='hug', aliases=['cuddle'])
	async def hug(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None or user == ctx.author:
			await ctx.reply('Sorry, i dont facilitate self-hugging.')
			return
		else:
			a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
			webhook = await ctx.channel.create_webhook(name = "UNamed")
			t = TenGiphPy.Tenor(token=tokens['tenor'])
			kiss_gif = await t.arandom("anime hug")
			embed=discord.Embed(title = f"{ctx.author.name} hugs {user.name}", colour = discord.Colour.from_rgb(a,b,c)).set_image(url=kiss_gif)
			await webhook.send(content = user.mention, embed=embed , username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
			await webhook.delete()

	@commands.command(name='slap')
	async def slap(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None or user == ctx.author:
			await ctx.reply('Sorry, i dont facilitate self-slapping.')
			return
		else:
			a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
			webhook = await ctx.channel.create_webhook(name = "UNamed")
			t = TenGiphPy.Tenor(token=tokens['tenor'])
			kiss_gif = await t.arandom("anime slap")
			embed=discord.Embed(title = f"{ctx.author.name} slaps {user.name}", colour = discord.Colour.from_rgb(a,b,c)).set_image(url=kiss_gif)
			await webhook.send(content = user.mention, embed=embed , username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
			await webhook.delete()

	@commands.command(name='pat')
	async def pat(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None or user == ctx.author:
			await ctx.reply('Sorry, i dont facilitate self-patting.')
			return
		else:
			a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
			webhook = await ctx.channel.create_webhook(name = "UNamed")
			t = TenGiphPy.Tenor(token=tokens['tenor'])
			kiss_gif = await t.arandom("anime pat")
			embed=discord.Embed(title = f"{ctx.author.name} pats {user.name}", colour = discord.Colour.from_rgb(a,b,c)).set_image(url=kiss_gif)
			await webhook.send(content = user.mention, embed=embed , username=ctx.author.display_name, avatar_url=ctx.author.avatar_url)
			await webhook.delete()

	@commands.command(name='ghostping', aliases = ['gp'])
	async def gp(self, ctx, *, member:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if member == None:
			await ctx.reply('Who do i ghost ping???')
			return
		x = await ctx.send(member.mention)
		await x.delete()
		await ctx.message.delete()

	@commands.command(name='pp')
	async def pp(self, ctx, user:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if user == None:
			user = ctx.author
		pp_range = random.randrange(0,10)
		equal = []
		for i in range(pp_range):
			equal.append('=')
		final = str(equal).replace('[', '').replace(']','').replace(',','').replace('\'', '').replace(' ','')
		em = discord.Embed(title = f"{user.name}'s PP Size",description = f"8{final}D")
		await ctx.send(embed=em)

	@commands.command(name = "ehelp", brief ="economy commands")
	async def ehelp(self, ctx):
		print("sent values")

	@commands.command(name='coolrate', brief = 'Rates how cool you/someone is', description = 'Rates how cool you/someone is\nSyntax //coolrate [person if you want to simprate someone]')
	async def coolrate(self, ctx, *, torate=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if torate == None:
			torate = ctx.author.display_name
		percent = random.randrange(0,100)
		if ctx.author == 831368744709783572:
			gembed = discord.Embed(title = 'CoolRate Machine', description = f"{torate} is 100% Cool :sunglasses:", colour = 00000)
			await ctx.send(embed=gembed)
		gembed = discord.Embed(title = 'CoolRate Machine', description = f"{torate} is {percent}% Cool :sunglasses:", colour = 00000)
		await ctx.send(embed=gembed)
	@commands.command()
	async def guessgender(self,ctx,torate:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if torate == None:
			torate = ctx.author
		percent = random.randrange(0,100)
		gender = ["boy","girl"]
		gender = random.choice(gender)
		await ctx.send(f"I am {percent} sure {torate.name} is a {gender}")
	async def gayrate(self, ctx, *, torate:discord.Member=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if torate == None:
			torate = ctx.author
		percent = random.randrange(0,100)
		gembed = discord.Embed(title = 'GayRate Machine', description = f"{torate.display_name} is {percent}% Gay :gay_pride_flag:", colour = discord.Colour.blurple())
		await ctx.send(embed=gembed)

	@commands.command(name = 'flipacoin', brief = 'Flips coins', description = 'Flips a requested number of coins and gives you the outcome', aliases = ['flipcoin', 'tosscoin', 'tossacoin'])
	async def flipacoin(self, ctx, number=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		if number == None:
			ans = random.choice(['Heads', 'Tails'])
			embed=discord.Embed(title = 'Flipped A Coin', description = ans, color = discord.Color.green())
			await ctx.send(embed=embed)
		else:
			number = int(number)
			answers = []
			for i in range(number):
				num = random.choice(['Heads', 'Tails'])
				answers.append(num)
			ans = str(answers)
			ans = ans.replace('[', '')
			ans = ans.replace(']', '')
			ans = ans.replace('\'', '')
			embed=discord.Embed(title = 'Outcomes', description =ans, color = discord.Color.magenta())
			await ctx.send(embed=embed)


	@commands.command(name='8ball', brief = 'Tells you your future', description = 'Tells you your future based on random choice\nSyntax //8ball [person if you want to simprate someone]', aliases = ['ask8', 'magic8'])
	async def magic_8_ball(self, ctx, *, question=None):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		random_answers = ['No Doubt', 'My sources tell me YES', 'You can rely on that', 'Better not tell you', 'Reply Hazy, Try Again', 'Nah, I wouldn\'t keep my hopes high on that', 'Highly Doubtful', 'Hell No']
		if question == None:
			await ctx.reply('Ask a question so that i can reply to it smh')
			return
		embed=discord.Embed(description=random.choice(random_answers), colour = discord.Color.blurple())
		embed.set_author(name = question, icon_url = ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(pass_context=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def meme(self, ctx):
		pkg = "fun"
		check = await checkpkg(ctx.guild.id,pkg)
		if check == "enabled":
			print("enabled")
		if check == "disabled":
			await ctx.send("command disabled, use mpkg to reinstall")
			return
		a,b,c = random.randint(0,255), random.randint(0,255), random.randint(0,255)
		embed = discord.Embed(title="A Meme...", description="[Latest Memes](https://www.reddit.com/r/dankmemes/new)", colour = discord.Colour.from_rgb(a,b,c))
		async with aiohttp.ClientSession() as cs:
			async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
				res = await r.json()
				embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(fun(bot))