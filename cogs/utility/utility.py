import discord, json, random, asyncio, pytz
from discord.ext import commands
#from googletrans import Translator
from discord import utils
import importlib
from discord import Webhook, RequestsWebhookAdapter, File
from anime_downloader.sites import get_anime_class
from datetime import datetime
import wikipedia
import requests
import TenGiphPy
#import translators as ts
from prsaw import RandomStuff
#from googlesearch import search
import time
#from bs4 import *
import bs4
import urllib.request
from library import funcs
import os

async def get_time_data():
	with open('data/times.json','r') as f:
		guilds = json.load(f)

	return guilds

async def open_time(guild):

	guilds = await get_time_data()

	if str(guild.id) in guilds:
		return False
	else:
		guilds[str(guild.id)] = {}
		guilds[str(guild.id)]["timezone"] = None

	with open('data/times.json','w') as f:
		json.dump(guilds,f)

	return True

#from db import post_search_data, fetch_search_data
#from search import search_main #check msgs
devs = ['775198018441838642', '750755612505407530', '746904488396324864']
tokens = {'tenor': 'BDE8TTQAN0H1'} 
class utility(commands.Cog, name='Utility'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def sticky(self,ctx,channelid,*,msg=None):
		channelid = channelid.replace("<#","")
		channelid = channelid.replace(">","")
		try:
			channel = int(channelid)
		except:
			return await ctx.send("please enter a channel id or channel")
		if msg == None:
			return await ctx.send("please eneter in this syntax, `<prefix>sticky <channelid> <message>`")
		with open("data/sticky.json","r") as f:
			st = json.load(f)
		st[str(channelid)] = msg
		with open("data/sticky.json","w") as z:
			json.dump(st,z)
		await ctx.send(f"Successfully stickied {msg} to <#{channelid}>")
	@commands.command()
	async def tp(self,ctx,action,id=None,tag=None):
		with open("data/tp.json","r") as f:
			tpj = json.load(f)
		if str(ctx.author.id) not in tpj:
			tpj[str(ctx.author.id)] = {}
			with open("data/tp.json","w") as z:
				json.dump(tpj,z)
		if action == "+" or action == "add":
			if id == None:
				return await ctx.send("please enter a channel id or channel")
			if tag == None:
				return await ctx.send("Please enter a name for that channel / channel id")
			id = id.replace("<#","")
			id = id.replace(">","")
			try:
				int(id)
			except:
				return await ctx.send("please enter a valid channel/ channel id")
			tpj[str(ctx.author.id)][tag] = id
			with open("data/tp.json","w") as z:
				json.dump(tpj,z)
			return await ctx.send(f"successfully added <#{id}> to tp")
		
		if action == "-" or action == "remove":
			if id == None:
				return await ctx.send("please enter a alias for the channel id to delete")
			try:
				del tpj[str(ctx.author.id)][id]
			except KeyError:
				return await ctx.send("tag not found")
			with open("data/tp.json","w") as z:
				json.dump(tpj,z)
			await ctx.send("Successfully deleted alias")
		
		if action != "+" and action != "-" and action != "add" and action != "remove":
			try:
				channelid = tpj[str(ctx.author.id)][action]
			except KeyError:
				return await ctx.send("unable to find tag")
			await ctx.send(f"<#{channelid}>")
			

	@commands.command(name='chatstart', aliases=['chat'])
	async def _chat(self,ctx, times:int=None):
		if times == None:
			times = 5
		if times > 50:
			return await ctx.send('Max is 50...')
			
		rs = RandomStuff(async_mode = True)

		embed = discord.Embed(title='ChatBot AI Engaged', description = f'Start sending messages and i will keep replying to the first `{times}` messages!\nSend `cancel` to cancel this chat session!', color=discord.Color.green())
		await ctx.send(embed=embed)
		def check(message):
			return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
		for i in range(times):
			if i == times-1:
				embed = discord.Embed(title='Oh No! This Chat Session has concluded!', description = 'If you want a longer session, use _chat <number of messages>!', colour = discord.Color.green())
				return await ctx.send(embed=embed)
			msg = await self.bot.wait_for('message', check=check)
			if msg.content.lower() == 'cancel':
				embed = discord.Embed(title='Canceled this Chat Session', description = 'Hope you liked me! Bye!', colour = discord.Color.green())
				return await ctx.send(embed=embed)
			res = await rs.get_ai_response(msg.content)
			if msg.content.lower() == 'who made you':
				res = 'I was made by PGAMERX and incorporated into Cerebrus by the Devs!'
			embed = discord.Embed(title=msg.content, description = res, colour = discord.Color.green())
			embed.set_footer(text=f'Chatting with {ctx.author.name} | Powered by AI', icon_url=ctx.author.avatar_url)
			embed.timestamp=datetime.datetime.utcnow()
			await ctx.send(embed=embed)

	@commands.command()
	async def modmail(self,ctx):
		exiter = False
		modmail_channel = discord.utils.get(self.bot.get_all_channels(), name="modmail")
		while exiter != True:
			try:
				choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				#choice2 = await self.bot.wait_for("message", check = lambda msg: ctx.channel.id == modmail_channel, timeout = 30)
				await modmail_channel.send(f"{ctx.author.name}: " + choice.content)
				#await ctx.author.send(choice2.content)
			except asyncio.TimeoutError or choice.content.startswith("exit"):
				exiter = True
				await ctx.author.send("modmail closed")
				await modmail_channel.send("modmail closed")


	@commands.command(name='time')
	async def time(self, ctx, user,*, timezone=None):
		try:
			try:
				user = await self.bot.get_user(user)
			except:
				user = str(user)
				if '!' in user:
					userid = user.replace('<@!', '').replace('>','')
				else:
					userid = user.replace('<@','').replace('>','')
				user=await self.bot.get_user(userid)
		except:
			user = ctx.author
		await open_time(user)
		users= await get_time_data()
		if users[str(user.id)]["timezone"] == None:
			if user == ctx.author:
				return await ctx.send('You don\'t have your time zone set.\nSet it using `_timeset (timezone)`')
			return await ctx.send('This user doesn\'t have their timezone set.\nAsk them to set it using `_timeset (timezone)`')
		elif users[str(user.id)]["timezone"] != None:
			zone = users[str(user.id)]["timezone"]
			zone = pytz.timezone(zone)
			time = datetime.now(zone)
			final=f'The Current Time in {zone} is:\n'+time.strftime('**%-I:%M %p, %d-%b-%Y %Z (UTC%z)**')
			return await ctx.send(final)

	@commands.command(name='timeset')
	async def timeset(self, ctx, *, timezone):
		user = ctx.author
		time_dict = {"ist":"Asia/Kolkata", "cet":"Europe/Africa", "india":"Asia/Kolkata"}
		if timezone.lower() in time_dict:
			timezone = time_dict[timezone]
		users = await get_time_data()
		try:
			zone = pytz.timezone(timezone)
		except pytz.exceptions.UnknownTimeZoneError:
			return await ctx.send('Unknown Timezone.\nRefer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones')
		users[str(user.id)]["timezone"] = str(zone)
		with open('data/times.json','w') as f:
			json.dump(users,f)
		time = datetime.now(zone)
		final=f'**I Have set your Timezone <a:pd_Check:841921292773228585>**\nThe Current Time in {str(zone)} is:\n'+time.strftime('**%-I:%M %p, %d-%b-%Y %Z (UTC%z)**')
		await ctx.send(final)

	@commands.command(name='wikipedia')
	async def wikipedia(self, ctx, *, query:str):
		query = wikipedia.search(query)[0]
		sp = wikipedia.page(query)
		embed = discord.Embed(title=sp.title, url=sp.url, description=wikipedia.summary(query, sentences=5))
		await ctx.send(embed=embed)
	@commands.command()
	async def embed(self,ctx,title,colors,*,args):
		await ctx.message.delete()
		sixteenIntegerHex = int(colors.replace("#", ""), 16)
		readableHex = int(hex(sixteenIntegerHex), 0)
		embed = discord.Embed(title=title,description=args,color=readableHex)
		await ctx.send(embed=embed)

	@commands.command(aliases=["ship"])
	async def lovecalc(self,ctx,user1:discord.Member,user:discord.Member=None):
		if user == None:
			user = user1
			user1 = ctx.author
		url = "https://love-calculator.p.rapidapi.com/getPercentage"

		querystring = {"fname":user1.name,"sname":user.name}

		headers = {
				'x-rapidapi-key': "a5b0325a1dmsh8e6bcbe244a2c36p1716e9jsn50d33c6c7737",
				'x-rapidapi-host': "love-calculator.p.rapidapi.com"
				}

		response = requests.request("GET", url, headers=headers, params=querystring)
		print(response.text) # make ship name by combining their names pls
		response = response.json()
		col = response["percentage"]
		comment = response["result"]
		embed = discord.Embed(title="Love calc",description = f"**{user1.name}** x **{user.name}**\nChance of love: `{col}%`\n{comment}!",color = ctx.author.color)
		await ctx.send(embed=embed)



	@commands.command(name='weather')
	async def weather(self, ctx, country:str=None):
		if country == None:
			return await ctx.reply('Which city?')
			return
		url = f'https://api.openweathermap.org/data/2.5/weather?q={country}&appid=2dc626e87a61e83e6b81715dd2c90e40'
		response = requests.request("GET", url)
		print(response.text)
		response = response.json()
		weather = response["weather"][{"main"}]
		description = response["weather"][{"description"}]
		embed = discord.Embed(title = "Weather",description = f"Weather : {weather}\n ~ {description}",color = discord.Color.green())
		await ctx.send(embed=embed)

	@commands.command(name='covidstats')
	async def covidstats(self,ctx,country=None):
		if country != None:
			country = country.capitalize()
		if country == None:
			country = "GLOBAL"
		url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

		querystring = {"country":country}

		headers = {
			'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
			'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
			}

		response = requests.request("GET", url, headers=headers, params=querystring)
		print(response.text)
		response = response.json()
		if response["message"] == "Country not found":
			await ctx.send("Country not found switching to global")
		rec = response["data"]["recovered"]
		ded = response["data"]["deaths"]
		conf = response["data"]["confirmed"]
		lc = response["data"]["lastChecked"]
		embed = discord.Embed(title = "Covid Stats",description = f"**Recovered:** {rec}\n**Deaths:** {ded}\n**Confirmed Cases:** {conf}\n**Last checked:** {lc}",color = discord.Color.green())
		await ctx.send(embed=embed)
		
	@commands.command(name='anime')
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def anime(self,ctx,*,key:str):
		main = await ctx.send('Fetching Anime from MyAnimeList...')
		await ctx.channel.trigger_typing()

		subtype = None

		if '--' in key:
			list = key.split(' --')
			print(list)
			key = list[0]
			subtype = list[1]

		if subtype == None:
			await funcs.get_anime_bysearch(ctx,main,key)

		elif subtype in 'reviews' or subtype in 'revs':	
			malid = await funcs.get_malid(key)
			await main.edit(content='Fetched Anime, Fetching Review')
			res = await funcs.get_reviews(malid)
			key = await funcs.get_title(key)
			poster = await funcs.get_poster(key)
			imdb = await funcs.fetch_imdb_rating(key)
			malscore = await funcs.get_score(key)
			user = res["reviewer"]["username"]
			url = res["url"]
			scores = res['reviewer']["scores"]
			try:
				rev = res['content'][0:1500]
			except:
				rev=res['content'][0:200]
			embed = discord.Embed(title=f"Review by {user}",  url=url, description = f"{rev} [Full Review]({url})", colour = discord.Color.green())
			embed.add_field(name='Scores Given', value = f'Overall: {scores["overall"]}\nStory: {scores["story"]}\nAnimation: {scores["animation"]}\nSound: {scores["sound"]}\nEnjoyment: {scores["enjoyment"]}')
			embed.add_field(name='Original Scores', value = f':star: **IMDb: **{imdb}/10\n:star: **MyAnimeList:** {malscore}/10')
			embed.set_thumbnail(url=poster)
			await main.edit(content=None,embed=embed)

		elif subtype in 'episodes' or subtype in 'eps':
			malid = await funcs.get_malid(key)
			name = await funcs.get_title(key)
			eps = await funcs.get_episodes(malid)
			poster = await funcs.get_poster(name)
			plot = await funcs.get_summary(name)
			tot = await funcs.get_tot_episodes(malid)
			await main.edit(content='Fetched Anime, Fetching Episodes... (this may take upto 1 minute)')
			titles = []
			links = []
			site = get_anime_class("animixplay")
			search = site.search(name)
			i = 0
			for ep in eps:
				titles.append(eps[i]["title"])
				url = search[0].url + f"/ep{i+1}"
				links.append(url)
				i += 1
			final = ''
			url_more = search[0].url
			i = 0
			await main.edit(content='Fetched Episodes... Writing Embed...')
			for link in links:
				final += f'**{i+1})** [{titles[i]}]({links[i]})\n'
				i += 1
			url = await funcs.get_url(name) + "/episode"
			embed = (discord.Embed(title=f"{name} - Episodes", url = url, description = f"{final}\n[More Episodes]({url_more})", colour = discord.Color.green())
			.set_author(name=f'Displaying First {len(links)} of {tot} Episode(s)')
			.add_field(name='Plot', value = plot)
			.set_thumbnail(url=poster))
			await main.edit(content=None,embed=embed)
	@commands.command(name='google')
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def google(self, ctx, *, query):
		url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyB5v5rcy5tgL3Z1oL2aU9DFOCVaHKKQoVI&cx=a0bb8145f553ecf5c&q={query}"

		response = requests.request("GET", url)

		response = response.json()
		results = response["items"][0:5]
		titles = []
		links = []
		snippets = []
		short_links = []
		for result in results:
			titles.append(result["title"])
			links.append(result["link"])
			snippets.append(result["snippet"])
			short_links.append(result["displayLink"])
		final = ''
		i = 0
		for title in titles:
			final += f'**{i+1})** [{title}]({links[i]})\n*Website: {short_links[i]}*\n{snippets[i]}\n\n'
			i += 1
		embed = (discord.Embed(title='Top 5 Results on Google', description = f"{final}[More Results](https://google.com/search?q={query.replace(' ','+')})", colour = discord.Color.green())
		.set_thumbnail(url='https://cdn.discordapp.com/attachments/827413229273088042/840897309742071828/Google__G__Logo.svg.png'))
		await ctx.send(embed=embed)

	@commands.command(name='movie')
	async def movie(self,ctx,*,key:str):
		import requests
		await ctx.channel.trigger_typing()

		url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/{key}"

		headers = {
			'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
			'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
			}

		response = requests.request("GET", url, headers=headers)
		response = response.json()
		id = response["titles"][0]["id"]
		url2 = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{id}"

		headers2 = {
			'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
			'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
			}

		response = requests.request("GET", url2, headers=headers2)
		response = response.json()
		plot = response['plot']
		url = f"https://www.imdb.com/title/{id}"
		score = response['rating']
		poster = response['poster']
		title = response['title']
		animix = get_anime_class('putlockers.com')
		runtime = response['length']
		search = animix.search(key)
		try:
			embed = discord.Embed(title = title,url=url,description=f"{plot}\n\n**Score:** :star: {score}/10 (IMDb)\n**Duration:** {runtime} (Movie or Each Episode)\n**Watch:** [Putlockers - May be Incorrect]({search[0].url})", colour=discord.Color.green())
		except:
			embed = discord.Embed(title = title,url=url,description=f"{plot}\n\n**Score:** :star: {score}/10 (IMDb)\n**Duration:** {runtime} (Movie or Each Episode)", colour=discord.Color.green())
		embed.set_thumbnail(url=poster)
		embed.timestamp = datetime.utcnow()
		embed.set_author(name='Powered by IMDb', url = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.imdb.com%2Fpressroom%2Fbrand-guidelines%2F&psig=AOvVaw0Iigy1GRzrL6LeLSDY83b9&ust=1620364676739000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMj-nvqmtPACFQAAAAAdAAAAABAD')
		embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name='animesearch')
	async def animesearch(self, ctx, *, keyword):
		animix = get_anime_class('animixplay.to')
		search = animix.search(str(keyword))
		links = []
		names = []
		for i in range(5):
			try:
				links.append(search[i].url)
				names.append(search[i].title)
			except:
				try:
					return await ctx.send(f'Very Sorry, could not gather enough results.\nHere is the top one:\n{search[0].title}: {search[0].url}')
				except:
					return await ctx.send(f'Very Sorry, could not find any results')
		links=links[:5]
		names=names[:5]
		final_text = f"[{names[0]}]({links[0]})\n[{names[1]}]({links[1]})\n[{names[2]}]({links[2]})\n[{names[3]}]({links[3]})\n[{names[4]}]({links[4]})"
		token = "BDE8TTQAN0H1"
		t = TenGiphPy.Tenor(token=token)
		poster = await t.arandom(str(keyword))
		embed = discord.Embed(title=f'Top 5 Results for \'{keyword}\' on AnimixPlay', description = final_text, colour=discord.Color.green())
		embed.set_image(url=poster)
		await ctx.send(embed=embed)

	@commands.command(name='putlockers', aliases=['moviesearch'])
	async def moviesearch(self, ctx, *, keyword):
		animix = get_anime_class('putlockers.com')
		search = animix.search(str(keyword))
		links = []
		names = []
		for i in range(3):
			try:
				links.append(search[i].url)
				names.append(search[i].title)
			except:
				try:
					return await ctx.send(f'Very Sorry, could not gather enough results.\nHere is the top one:\n{search[0].title}: {search[0].url}')
				except: # @ace is god
					return await ctx.send(f'Very Sorry, could not find any results')
		links=links[:5]
		names=names[:5]
		final_text = f"[{names[0]}]({links[0]})\n[{names[1]}]({links[1]})\n[{names[2]}]({links[2]})"
		token = "BDE8TTQAN0H1"
		t = TenGiphPy.Tenor(token=token)
		poster = await t.arandom(str(keyword))
		embed = discord.Embed(title=f'Top 3 Results for \'{keyword}\' on Putlockers', description = final_text, colour=discord.Color.green())
		embed.set_image(url=poster)
		await ctx.send(embed=embed)

	@commands.command(aliases=["ph"])
	async def postheist(self,ctx):
		ping = None
		embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "(a)dvert or (e)mbed?")
		await ctx.send(embed=embed)
		try:
			choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
			if choice.content.lower() == "embed" or choice.content.lower() == "e":
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist Post'",description = "Guild id?")
				await ctx.send(embed=embed)
				choice2 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				guildid = choice2.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist Post'",description = "Content and/or message?")
				await ctx.send(embed=embed)
				choice6 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				content = choice6.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist Post'",description = "Invite? (include `https://`)")
				await ctx.send(embed=embed)
				choice5 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				invite = choice5.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "Which channel?")
				await ctx.send(embed=embed)
				choice3 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				channel = choice3.content
				channelid = channel.replace('<#','')
				channelid = channelid.replace('>','')
				channel = ctx.guild.get_channel(int(channelid))
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "Ping?\n`here`,`everyone` or `role id`")
				await ctx.send(embed=embed)
				choice4 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice4.content.lower() == "here":
					ping = "@here"
				if choice4.content.lower() == "everyone":
					ping = "@everyone"
				else:
					ping = "<@" + choice4.content + ">"
				await ctx.send("post heist? `y`/`n`")
				choice8 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice8.content.lower() == "y":
					embed = discord.Embed(title = f"Heist Time",description = f"id: {guildid}\n**Message:**\n{content}\n**[Join Server]({invite})**")
					await channel.send(embed=embed)
					await channel.send(ping)
					return
				if choice8.content.lower == "n":
					await ctx.send("cancelled")
					return
			if choice.content.lower() == "advert" or choice.content.lower() == "a":
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "Send advert")
				await ctx.send(embed=embed)
				choice2 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				advert = choice2.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "Which channel?")
				await ctx.send(embed=embed)
				choice3 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				channel = choice3.content
				channelid = channel.replace('<#','')
				channelid = channelid.replace('>','')
				channel = ctx.guild.get_channel(int(channelid))
				embed = discord.Embed(title=f"{ctx.guild.name}'s Heist'",description = "Ping?\n`here`,`everyone` or `role id`")
				await ctx.send(embed=embed)
				choice4 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice4.content.lower() == "here":
					ping = "@here"
				if choice4.content.lower() == "everyone":
					ping = "@everyone"
				else:
					ping = "<@" + choice4.content + ">"
				await ctx.send("post heist? `y`/`n`")
				choice7 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice7.content.lower() == "y":
					await channel.send(advert)
					await channel.send(ping)
					return
				if choice7.content.lower == "n":
					await ctx.send("cancelled")
					return
		except asyncio.TimeoutError:
			await ctx.send("response not done...")
	@commands.command(aliases=["pop"])
	async def postpartner(self,ctx):
		try:
				embed = discord.Embed(title=f"{ctx.guild.name}'s Partnership'",description = "Send advert")
				await ctx.send(embed=embed)
				choice2 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				advert = choice2.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Partnership'",description = "Invite? (include `https://`)")
				await ctx.send(embed=embed)
				choice9 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				invite = choice9.content
				embed = discord.Embed(title=f"{ctx.guild.name}'s Partnership'",description = "Which channel?")
				await ctx.send(embed=embed)
				choice3 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				channel = choice3.content
				channelid = channel.replace('<#','')
				channelid = channelid.replace('>','')
				channel = ctx.guild.get_channel(int(channelid))
				embed = discord.Embed(title=f"{ctx.guild.name}'s Partnership'",description = "Ping?\n`here`,`everyone` or `role id`")
				await ctx.send(embed=embed)
				choice4 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice4.content.lower() == "here":
					ping = "@here"
				if choice4.content.lower() == "everyone":
					ping = "@everyone"
				else:
					ping = "<@" + choice4.content + ">"
				await ctx.send("post partner? `y`/`n`")
				choice7 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				if choice7.content.lower() == "y":
					embed = discord.Embed(title="Invite",description=f"{advert}\n**[Join Server]({invite})**")
					await ctx.send(embed=embed)
					await channel.send(ping)
					return
				if choice7.content.lower == "n":
					await ctx.send("cancelled")
					return
		except asyncio.TimeoutError:
			await ctx.send("not responded")
	@commands.command()
	async def poll(self,ctx,*,poll):
		await ctx.message.delete()
		embed = (discord.Embed(title=f"{ctx.author.name}'s poll",description = f"{poll}",color = discord.Color.green()))
		pollmsg = await ctx.send(embed=embed)
		await pollmsg.add_reaction("👍")
		await pollmsg.add_reaction("👎")
	@commands.command(aliases=["download"])
	async def dl(self,ctx,link,filename=None):
		if filename == None:
			await ctx.send("Enter dl syntax eg `_dl link filename`,`_dl https://google.com/index.html index.html`")
			return
		await os.system(f"wget {link}")
		await os.system(f"mv {filename} static/downloads/")
		await ctx.send(f"download link for 1m\nhttps://Cerebus.he1ios.repl.co/static/downloads/{filename}")
		await asyncio.sleep(60)
		await os.system(f"rm -rf static/downloads/{filename}")
		return
	@commands.command()
	async def run(self,ctx,language,linktofile,filename):
		os.system(f"cd run && wget {linktofile}")
		if language == "py":
			os.system(f"python run/{filename}")
			os.system(f"rm -rf run/{filename}")
		
	@commands.command(aliases=["starth"])
	async def startheist(self,ctx):
		try:
			reply = await self.bot.wait_for("message", check=None, timeout = 20)
		except asyncio.TimeoutError:
			await ctx.send("no heist detected")
		if reply.content.startswith("pls heist"):
			tmr = "60"
			timer = int(tmr)
			tmr2 = str(timer)
			timsg = await ctx.send(f"Timer:\n**{tmr2}**")
			await ctx.send("Type `join heist` to steal some cazh")
			while timer != 0 or timer < 0:
				timer -= 1
				tmr2 = str(timer)
				await asyncio.sleep(1)
				await timsg.edit(content=f"Timer:\n**{tmr2}**")
				await asyncio.sleep(1)
				await ctx.send(f"{ctx.author.mention} heist's up")
			else:
				await ctx.send("no heist detected")
	@commands.command()
	async def remind(self,ctx,timer,reminder):
		timer = int(timer)
		while timer != 0 or timer > 0:
			await asyncio.sleep(1)
			timer-=1
		if timer == 0:
			await ctx.author.send(reminder)
	@commands.command()
	async def timer(self,ctx,tmr):
		timer = int(tmr)
		tmr2 = str(timer)
		timsg = await ctx.send(f"Timer:\n**{tmr2}**")
		while timer != 0 or timer < 0:
			timer -= 1
			tmr2 = str(timer)
			await asyncio.sleep(1)
			await timsg.edit(content=f"Timer:\n**{tmr2}**")
			await asyncio.sleep(1)
		await ctx.send(f"{ctx.author.mention} Time's up")
			
	@commands.command(pass_context=True,aliases=["sn","nick"])
	@commands.has_permissions(manage_guild=True)
	async def setnick(self,ctx, user: discord.Member,*, args=None):
			if args == None:
				await user.edit(nick=None)
				embed = (discord.Embed(title="Nickname Change",description = f" changed **{user.mention}'s** nickname to **{user.name}**"))
				await ctx.send(embed=embed)
				return

			await user.edit(nick=args)
			embed = (discord.Embed(title="Nickname Change",description = f" changed **{user.mention}'s** nickname to **{args}**"))
			await ctx.send(embed=embed)
			return
			
	@commands.command(aliases=["taxcalc"])
	async def tc(self,ctx,amount):
		amount = int(amount)
		calcamount = amount*0.08
		neededamount = amount + calcamount
		embed = (discord.Embed(title = "Cerebrus Taxcalc",description=f"amount : `{str(amount)}`\n tax: `{str(calcamount)}`\nneeded amount : `{str(neededamount)}`",color = discord.Color.green()))
		await ctx.send(embed=embed)
		return
	@commands.command()
	async def calc(self,ctx,no1,sign,no2):
		no1 = int(no1)
		no2 = int(no2)
		if sign == "*":
			ans = no1 * no2
		if sign == "/":
			ans = no1 / no2
		if sign == "+":
			ans = no1 + no2
		if sign == "-":
			ans = no1 - no2
		embed = (discord.Embed(title="Cerebrus Calculator",description=f"Qn : `{str(no1)} {sign} {str(no2)}`\nAns : `{str(ans)}`",color = discord.Color.green()))
		await ctx.send(embed=embed)
		return
		


	@commands.command(name='slowmode', brief = 'Toggles Slowmode', description = 'Sets/Removes the Slowmode of a channel\nMake sure to mention to remove it or in seconds/minutes/hours\nE.g. 2s/2m/2h', aliases = ['sm'])
	async def slowmode(self, ctx, no_time):
		if ctx.author.guild_permissions.manage_channels == True:
			if 'remove' in no_time or no_time == '0':
				await ctx.channel.edit(slowmode_delay=0)
				await ctx.channel.send(f'The Slowmode has been removed.')
			elif 's' in no_time:
				t = no_time.strip('s')
				t = int(t)
				f_time = int(t)
				if t == 0:
					await ctx.send(f'The Slowmode has been removed.')
				else:
					await ctx.send(f'The Slowmode is now {t} seconds.')

			elif 'h' in no_time:
				t = no_time.strip('h')
				t = int(t)
				f_time = int(t * 3600)
				await ctx.send(f'The Slowmode is now {t} hours.')

			elif 'm' in no_time:
				t = no_time.strip('m')
				t = int(t)
				f_time = int(t * 60)
				await ctx.send(f'The Slowmode is now {t} minutes.') 
			if f_time > 21600:
				await ctx.reply('Cant set slowmode beyond 6 hours.')
				return
			await ctx.channel.edit(slowmode_delay=f_time)
		else:
			await ctx.delete()
			return
	@commands.command(name='choose')
	async def choose(self, ctx, option1, option2, option3=None, option4=None, option5=None):
		options = [option1, option2, option3, option4, option5]
		print(options)
		for option in options:
			if option == None:
				options.remove(option)
			else:
				pass
		print(options)
		options.remove(None)
		ans = random.choice(options)
		options = str(options)
		options = options.replace('[', '')
		options = options.replace(']', '')
		options = options.replace('\'', '')
		embed=discord.Embed(description=f"I Choose... {ans}!", colour = discord.Color.blurple())
		embed.set_author(name = options, icon_url = ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name='whois',aliases=["i"])
	async def whois(self, ctx, user:discord.Member=None):
		if user == None:
			user = ctx.author
		default = False
		if user.avatar == user.default_avatar:
			default = True
		embed = (discord.Embed(title = user.name, description = f'Complete Info\n\n**User ID:** {user.id}\n\n**User Status:** {user.status}\n**Default Avatar:** {default}\n**Created At:** {user.created_at} UTC\n**Joined At:** {user.joined_at}', colour = discord.Color.green())
		.set_thumbnail(url=user.avatar_url))
		await ctx.send(embed=embed)

	@commands.command(name='esm')
	@commands.has_any_role("・Event Manager")
	async def esm(self, ctx, no_time):
		if 'remove' in no_time or no_time == '0':
			await ctx.channel.edit(slowmode_delay=0)
			await ctx.channel.send(f'The Slowmode has been removed.')
		elif 's' in no_time:
			t = no_time.strip('s')
			t = int(t)
			f_time = int(t)
			if t == 0:
				await ctx.send(f'The Slowmode has been removed.')
			else:
				await ctx.send(f'The Slowmode is now {t} seconds.')

		elif 'h' in no_time:
			t = no_time.strip('h')
			t = int(t)
			f_time = int(t * 3600)
			await ctx.send(f'The Slowmode is now {t} hours.')

		elif 'm' in no_time:
			t = no_time.strip('m')
			t = int(t)
			f_time = int(t * 60)
			await ctx.send(f'The Slowmode is now {t} minutes.') 
		if f_time > 21600:
			await ctx.reply('Cant set slowmode beyond 6 hours.')
			return
		await ctx.channel.edit(slowmode_delay=f_time)

	@commands.command(name='avatar', aliases=['av'])
	async def avatar(self, ctx, target:discord.Member=None):
		if target == None:
			target = ctx.author
		avem = discord.Embed(title = f'{str(target)}\'s Avatar',colour=discord.Color.green())
		avem.set_image(url=target.avatar_url)
		await ctx.send(embed=avem)
		return

	@commands.command(name='botsuggest', aliases = ['bot suggest'])
	async def botsuggest(self, ctx, *, args):
		f = open("suggestions.txt", "a")
		f.write("\n" + "- " + args + f"~ {ctx.author.display_name}")
		f.close()
		await ctx.send("Successfully Noted\nThanks for suggesting!")
		return
	
	@commands.command(name = 'webhook', brief = 'Say a message as another user', description = 'Say a message as another user using webhook', aliases=["sayas"])
	@commands.has_permissions(manage_guild=True)
	async def webhook(self, ctx, user:discord.Member=None, *,args=None):
		if user == None:
			await ctx.reply('Who may i say this as??')
			return
		if args ==None:
			await ctx.reply('What message should i send??')
			return
		else:
			await ctx.message.delete()
			webhook = await ctx.channel.create_webhook(name = "Cerebrus")
			xd1 = await webhook.send(args , username=user.display_name, avatar_url=user.avatar_url)
			await webhook.delete()
		if commands.has_permissons(manage_guild=False):
			await ctx.send("No permissons entry denied ;)")

	@commands.command(name = 'nopermhook', brief = 'Say a message as another user', description = 'Say a message as another user using webhook', aliases=["nopermsayas"])
	async def nopermhook(self, ctx, user:discord.Member=None, *,args=None):
		if ctx.author.id == devs[1]:
			if user == None:
				await ctx.reply('Who may i say this as??')
				return
			if args ==None:
				await ctx.reply('What message should i send??')
				return
			else:
				await ctx.message.delete()
				webhook = await ctx.channel.create_webhook(name = "UNamed")
				xd1 = await webhook.send(args , username=user.display_name, avatar_url=user.avatar_url)
				await webhook.delete()
		elif ctx.author.id == devs[2]:
			if user == None:
				await ctx.reply('Who may i say this as??')
				return
			if args ==None:
				await ctx.reply('What message should i send??')
				return
			else:
				await ctx.message.delete()
				webhook = await ctx.channel.create_webhook(name = "UNamed")
				xd1 = await webhook.send(args , username=user.display_name, avatar_url=user.avatar_url)
				await webhook.delete()
		elif ctx.author.id == devs[3]:
			if user == None:
				await ctx.reply('Who may i say this as??')
				return
			if args ==None:
				await ctx.reply('What message should i send??')
				return
			else:
				await ctx.message.delete()
				webhook = await ctx.channel.create_webhook(name = "UNamed")
				xd1 = await webhook.send(args , username=user.display_name, avatar_url=user.avatar_url)
				await webhook.delete()
		else:
			await ctx.send("You are not a developer wtf r u doing lol ~ Kaneki + Cerebus Team")

	@commands.command()
	async def gif(self, ctx, *, giftag):
		if ctx.guild.id == 799907027832537088:
			await ctx.send("blocked guild cuz of abuse to cmd")
			return
		"""This command will return a tenor gif to you"""
		token = ""
		t = TenGiphPy.Tenor(token=tokens['tenor'])
		getgifurl = await t.arandom(str(giftag))
		embed = discord.Embed(title = f"Result for '{giftag}' on Tenor")
		embed.set_image(url = getgifurl)
		await ctx.send(embed=embed)

	@gif.error
	async def tenor_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Giftag cant be None. Please give a valid giftag to search.')
		else:
			raise error

	@commands.command(name = "ghelp", brief = "gives the giveaway commands")
	async def ghelp(self, ctx):
		print("sent values")

	@commands.command(name='purge', brief = 'Purges messages', description = 'Purges the given number of messages')
	async def purge(self, ctx, lim):
		if ctx.author.guild_permissions.manage_messages == True:
			if lim == 'all':
				lim = 100
			lim = int(lim)
			if lim < 1:
				await ctx.delete()
				await ctx.channel.send(f'Mhmm. Pretty sure i can\'t purge less than 1 messages {ctx.author.mention}.')
			else:
				await ctx.channel.purge(limit=lim+1)
				x = await ctx.channel.send(f'Purged **{lim}** messages')
				await asyncio.sleep(3)
				await x.delete()
		else:
			await ctx.delete()
			return

	@commands.command(name='afk', brief = 'Sets an AFK for you', description = 'Sets an AFK so that whenever you are pinged an embed pops up dispaying your afk message')
	async def afk(self, ctx, action=None, *, afk_msg=None):
		user = ctx.author
		with open("data/afk.json", "r") as f:
			users = json.load(f)

		def open_afk(user):
			with open("data/afk.json", "r") as f:
				users = json.load(f)
			if str(user.id) in users:
				return False
			else:
				users[str(user.id)] = {}
				users[str(user.id)]["afk_status"] = False
				users[str(user.id)]["afk_msg"] = None
			with open("data/afk.json", "w") as f:
				json.dump(users, f)
			return True
		if afk_msg == None:
			afk_msg = 'Just AFK'
		open_afk(ctx.author)
		if action == 'set':
			users[str(user.id)]["afk_status"] = True
			users[str(user.id)]["afk_msg"] = afk_msg
			with open("data/afk.json", "w") as f:
				json.dump(users, f)
			embed=discord.Embed(title = 'Set Your AFK', description = afk_msg, color = discord.Color.magenta())
			embed.set_thumbnail(url = user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await ctx.send(embed=embed)
		elif action == 'edit':
			if users[str(user.id)]["afk_status"] != True:
				await ctx.reply('You don\'t have an AFK set\nSet it using `_afk set <afk>`')
				return
			users[str(user.id)]["afk_msg"] = afk_msg
			with open("data/afk.json", "w") as f:
				json.dump(users, f)
			embed=discord.Embed(title = 'Edited Your AFK', description = afk_msg, color = discord.Color.magenta())
			embed.set_thumbnail(url = user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await ctx.send(embed=embed)
		elif action == 'remove':
			if users[str(user.id)]["afk_status"] != True:
				await ctx.reply('You don\'t have an AFK set\nSet it using `-afk set <afk>')
				return
			users[str(user.id)]["afk_status"] = False
			users[str(user.id)]["afk_msg"] = None
			with open("data/afk.json", "w") as f:
				json.dump(users, f)
			embed=discord.Embed(title = 'Your AFK has been Removed', color = discord.Color.magenta())
			embed.set_thumbnail(url = user.avatar_url)
			embed.timestamp = datetime.utcnow()
			await ctx.send(embed=embed)
		else:
			await ctx.reply('Please provide an action.\nTo set an AFK, `<p>afk set <afk>`\nTo edit an AFK, `<p>afk edit <new_afk>`\nTo remove an AFK `<p>afk remove`')
def setup(bot):
    bot.add_cog(utility(bot))