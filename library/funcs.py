import discord, requests, asyncio, random, json, os, copy
from datetime import datetime
from anime_downloader.sites import get_anime_class
from discord.ext import commands
async def copy_context_with(ctx: commands.Context, *, author=None, channel=None, **kwargs):
	# copy the message and update the attributes
	alt_message: discord.Message = copy.copy(ctx.message)
	alt_message._update(kwargs)  # pylint: disable=protected-access

	if author is not None:
			alt_message.author = author
	if channel is not None:
			alt_message.channel = channel

	# obtain and return a context of the same type
	return await ctx.bot.get_context(alt_message, cls=type(ctx))
async def fetch_imdb_rating(key:str):
	url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/{key}"

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers)
	response = response.json()
	try:
		id = response["titles"][0]["id"]
	except:
		return 'Rating Unavailable'
	url2 = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{id}"

	headers2 = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
		}

	response = requests.request("GET", url2, headers=headers2)
	response = response.json()
	if response['rating'] == None or response['rating'] == ' ':
		return 'Rating Unavailable'
	else:
		return response['rating']

async def get_title(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['title']

async def get_score(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['score']

async def get_anime_bysearch(ctx,main,key:str):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	try:
		response = response["results"][0]
	except:
		return await main.edit(content='Could not find any results on MAL.')
	plot = response['synopsis']
	url = response['url']
	score = response['score']
	members = "{:,}".format(response['members'])
	poster = response['image_url']
	title = response['title']
	await main.edit(content=f'**Fetched Anime:** \n{title}: {url}\n\nFetching Available Watch Options...')
	watch_links = []
	possible_sites = ['animixplay','4anime', 'gogoanime', 'animerush','kissanimex', 'ryuanime']
	for site in possible_sites:
		ss = get_anime_class(site)
		try:
			search = ss.search(title)
		except:
			pass
		if len(search) == 0:
			pass
		else:
			if site == 'animixplay':
				watch_links.append(f"[AnimixPlay (recommended)]({search[0].url})")
			elif site == 'animerush':
				watch_links.append(f"[AnimeRush]({search[0].url})")
			elif site == 'gogoanime':
				watch_links.append(f"[GoGoAnime]({search[0].url})")
			elif site == 'kissanimex':
				watch_links.append(f"[KissAnime]({search[0].url})")
			elif site == 'ryuanime':
				watch_links.append(f"[RyuAnime]({search[0].url})")
			else:
				watch_links.append(f"[{site}]({search[0].url})")
	episodes = response['episodes']
	age = response['rated']
	final = str(watch_links)[1:-1]
	final = final.replace('\'','').replace(', ',' | ')
	imdb_score = await fetch_imdb_rating(title)
	await main.edit(content=f'Found Possible Watch Options for {title}\nCreating Embed...')
	await asyncio.sleep(3)
	try:
		embed = discord.Embed(title = title,url=url,description=f"{plot} [Full Synopsis]({url})\n\n**Episodes:** {episodes}\n**Age Rating:** {age}\n**Views:** {members}", colour=discord.Color.green())
		embed.add_field(name='Score', value = f':star: **IMDb:** {imdb_score}/10\n:star: **MyAnimeList:** {score}/10')
		embed.add_field(name='Stream Now (Pirated but Safe)', value = final, inline=False)
	except:
		embed = discord.Embed(title = title,url=url,description=f"{plot}[Full Synopsis]({url})\n\n**Score:** :star: {score}/10 (MyAnimeList)\n**Episodes:** {episodes}\n**Age Rating:** {age}\n**Views:** {members}\n**Watch:** Unavailable.", colour=discord.Color.green())
	embed.set_thumbnail(url=poster)
	embed.timestamp = datetime.utcnow()
	embed.set_author(name='Powered by MyAnimeList')
	embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
	await main.edit(content=None,embed=embed)

async def get_malid(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['mal_id']

async def get_poster(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['image_url']

async def get_url(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['url']

async def get_summary(key):
	url = "https://jikan1.p.rapidapi.com/search/anime"

	querystring = {"q":key}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = response.json()
	response = response["results"][0]
	return response['synopsis']

async def get_reviews(malid):
	url = f"https://jikan1.p.rapidapi.com/anime/{malid}/reviews"

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers)
	response = response.json()
	index = random.randrange(0,5)
	try:
		return response['reviews'][index]
	except IndexError:
		return response['reviews'][0]

async def get_episodes(malid):

	url = f"https://jikan1.p.rapidapi.com/anime/{malid}/episodes"

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers)
	eps = len(response.json()["episodes"])
	if eps <= 12:
		return response.json()["episodes"][0:eps]
	return response.json()["episodes"][0:12]

async def get_tot_episodes(malid):

	url = f"https://jikan1.p.rapidapi.com/anime/{malid}/episodes"

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "jikan1.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers)
	eps = len(response.json()["episodes"])
	return eps

async def send_help(bot,ctx, category = None):
	featured = (discord.Embed(title='New on Cerebrus', description = 'Commands that have been newly added to Cerebrus, keeps getting updated every day!', colour = discord.Color.green())
	.set_author(name='FEATURED', icon_url = ctx.author.avatar_url)
	.add_field(name='Anime', value = 'Get Info with watch options or reviews or episode stream now hyperlinks for any anime.\nUse `_help anime` for more info.', inline=False)
	.add_field(name='Google', value='Get Google\'s top 5 results on any topic!', inline=False)
	.add_field(name='Mpkg', value='Use a package manager to enable modules of Cerebrus', inline=False)
	.add_field(name='Riddle', value='Get a random riddle along with it\'s answer! ||(answer in spoiler)||', inline=False)
	.add_field(name='Time', value='Get the time for yours/somebody else\'s set-timezone!\n**WARNING:** Command still in BETA Testing!', inline=False)
	.add_field(name='Count and abc', value='a,b,c / 0,1,2. make a channel called `c-count` for counting and `c-abc` for abc',inline = False)
	.add_field(name='tp', value='teleport to channels. `<prefix>tp + <channelid> <alias>` `<prefix>tp - <alias>` `<prefix>tp <alias>`',inline = False)
	.add_field(name='Sticky', value='Sticky a message to a channel. eg. `<prefix>sticky <channel> <message>`',inline = False)
	.add_field(name='Coming Soon', value='Wikipedia: Search WikiPedia and get it\'s results.',inline = False))
	def get_guilds_data():
		with open('data/config.json','r') as f:
			guilds = json.load(f)

		return guilds
	guilds = get_guilds_data()
	try:
		prefix = guilds[str(ctx.guild.id)]["prefix"]
	except KeyError:
		prefix = "_"
	if category == None or category == 'all':
		embed1 = (discord.Embed(title = 'Fun',colour = discord.Color.green())
		.set_author(name = 'Help Menu | Page 1', icon_url = ctx.author.avatar_url)
		.add_field(name = '8ball', value = 'Magically get a reply for a question!')
		.add_field(name = 'Rate', value='`gayrate`, `simprate`, `coolrate` | Rate yourself or a mentioned user.', inline = False)
		.add_field(name = 'Interactive', value = '`hug`, `kiss`, `pat`, `slap` | Interact with users as if IRL', inline = False)
		.add_field(name = 'Meme', value = 'Get a nice, fresh meme.', inline = False)
		.add_field(name = 'Echo', value='Say a message through me.', inline = False))

		embed2 = (discord.Embed(title = 'Moderation', colour = discord.Color.green())
		.set_author(name = 'Help Menu | Page 2', icon_url = ctx.author.avatar_url)
		.add_field(name = 'Mute', value = 'Mute a Person [must set a Muterole]', inline = False)
		.add_field(name = 'Kick', value = 'Kick a User. Can Specify a reason too.', inline = False)
		.add_field(name = 'Ban', value = 'Ban a User. Can Specify Reason too.', inline = False)
		.add_field(name='Slowmode', value = 'Set the Slowmode for the channel.', inline=False)
		.add_field(name='Lock, Unlock, Lockdown', value = 'Lock and Unlock the Channel.\n`_lockdown` will lockdown a specific set of channels, use `_lds` to set it up.'))

		embed3 = (discord.Embed(title = 'Music', description = 'Listen to Music in a VC 🎶 **[Top Notch Quality]**', color = discord.Color.green())
		.set_author(name = 'Help Menu | Page 3', icon_url = ctx.author.avatar_url)
		.add_field(name = 'Play', value = 'Make the bot play a song straight from youtube in high quality.', inline = False)
		.add_field(name='Pause/Resume', value = 'Pause/Resume the current Song', inline=False)
		.add_field(name='Stop', value = 'Stop the song and clear the queue', inline=False)
		.add_field(name='Join/Leave', value = 'Make the Bot Join/Leave the VC you are in.', inline=False)
		.add_field(name='Volume', value='Lower/Increase the Volume of the music.'))

		embed4 = (discord.Embed(title = "Utility",color = discord.Color.green())
		.set_author(name = 'Help Menu | Page 4', icon_url = ctx.author.avatar_url)
		.add_field(name = "Thelp", value = "shows all ticketing commands in detail",inline = False)
		.add_field(name = "Ticket", value = "Create a New Ticket `_ticket <msg>` eg, `_ticket test`",inline = False)
		.add_field(name = "AddAccess", value = "Add access to a role/member",inline = False)
		.add_field(name = "Vouch", value = "Vouch for a user `_vouch <user>` eg, `_vouch @kaneki`",inline = False)
		.add_field(name = "Vouches", value = "Check your vouches or for a user `_vouches <user>` eg, `_vouches @kaneki`",inline = False)
		.add_field(name = "Vleaderboard", value = "Check vouch leaderboards eg `_vleaderboard`",inline = False)
		.add_field(name='Google', value = 'Google anything and get the top 5 results.'))

		embed5 = (discord.Embed(title = "Giveaways",color = discord.Color.green())
		.set_author(name = 'Help Menu | Page 5', icon_url = ctx.author.avatar_url)
		.add_field(name = "Gcancel", value = "cancels a giveaway `_gcancel <channel id> <message id>` eg, `_gcancel 811087796055965736 833560784964550676`",inline = False)
		.add_field(name = "Gstart", value = "start a giveaway `_gstart <seconds> <minutes> <hours> <prize>` eg, `_gstart 10 0 0 test`",inline = False)
		.add_field(name = "Gcreate", value = "create a giveaway with ease `_gcreate`",inline = False)
		.add_field(name = "Gend", value = "ends a giveaway `_gend <channel id> <message id>` eg, `_gend 811087796055965736 833560784964550676`",inline = False)
		.add_field(name = "Greroll", value = "rerolls a giveaway `_greroll <channel id> <message id>` eg, `_greroll 811087796055965736 833560784964550676`",inline = False)
		)
		embed7 = (discord.Embed(title = "Games",color = discord.Color.green())
		.set_author(name = 'Help Menu | Page 6', icon_url = ctx.author.avatar_url)
		.add_field(name = "Fight", value = "Starts a fight `_fight <user>` eg, `_fight @kaneki`",inline = False)
		.add_field(name = "TTT", value = "Starts a Tic Tac Toe game `_ttt <user>` eg, `_ttt @kaneki`",inline = False)
		.add_field(name = "RPS", value = "Rock paper scissors `_rps <user>` eg, `_rps @kaneki`",inline = False)
		.add_field(name="Chess", value="Starts a game of chess and asks the challenged user to accept/deny.")
		.add_field(name = "Battleship", value = "Classic Battleship Game `_battleship` eg, `_battleship`",inline = False)
		.add_field(name = "Coinflip", value = "Flip a coin",inline = False)
		)
		embed8 = (discord.Embed(title='Entertainment', colour = discord.Color.green())
		.set_author(name='Help Menu | Page 7', icon_url = ctx.author.avatar_url)
		.add_field(name='Anime', value = 'Get Info with watch options or reviews or episode stream now hyperlinks for any anime.\nUse `_help anime` for more info.', inline=False)
        .add_field(name="YTVC", value = 'Watch YouTube remotely, with friends, in a VC, discord BETA feature, only available to select servers, now available to you, through Cerebrus!\n**NOTE:** Slash-only command, type `/ytvc` and follow the guide!'))

		embed9 = (discord.Embed(title="Marry",color = discord.Color.green())
		.set_author(name='Help Menu | Page 8', icon_url = ctx.author.avatar_url)
		.add_field(name='Marry', value = 'Marries a user ')
		.add_field(name='Divorce', value = 'divorces a user ')
		.add_field(name='Adopt', value = 'Adopts a user ')
		.add_field(name='Disown', value = 'Disowns a user ')
		.add_field(name='Sibling', value = 'Makes a user your sibling')
		.add_field(name='Desibling', value = 'Disowns a user as your sibling')
		.add_field(name='Children', value = 'Shows your children')
		.add_field(name='Sex', value = 'Create a child with a name of your choice (NO NSFW AT ALL)')
		.add_field(name='Ship', value = 'Ships a user with another user')
		.add_field(name='Partner', value = 'Shows your partner')
		.add_field(name='Siblings', value = 'Shows your siblings')
		.add_field(name='Parent', value = 'Shows your parent')
		)	
		embed10 = (discord.Embed(title="Economy",color=discord.Color.green())
		.set_author(name='Help Menu | Page 9', icon_url = ctx.author.avatar_url)
		.add_field(name='Beg', value = 'Beg for money')
		.add_field(name='Scout', value = 'Scout for money')
		.add_field(name='Highlow', value = 'Highlow for money')
		.add_field(name='Snakeeyes', value = 'Gamble with dice')
		.add_field(name='Bet', value = 'bet on your life')
		.add_field(name='Balance', value = 'Check your money')
		.add_field(name='Withdraw', value = 'Withdraw money from your bank')
		.add_field(name='Deposit', value = 'Deposit money into your bank')
		.add_field(name='coinflip', value = 'Flip a coin you might get lucky')
		.add_field(name='Share', value = 'Send money to others')
		.add_field(name='Rob', value = 'Rob users, disabled using mpkg')
		.add_field(name='Heist', value = 'Rob users through their bank, disabled using mpkg')
		.add_field(name='Shop', value = 'A shop just for you')
		.add_field(name='Buy', value = 'Buy from the shop')
		.add_field(name='Gift', value = 'Share items')
		.add_field(name='Slots', value = 'Chink Chink Chink, CASH TIME')
		.add_field(name='Bag', value = 'Check your inventory')
		.add_field(name='Sell', value = 'Sell items')
		.add_field(name='Leaderboard', value = 'Global stats')
		.add_field(name='Use', value = 'Use an item')
		.add_field(name='Deposit', value = 'Deposit money into your bank')
		)
		embed11 = (discord.Embed(title= "Imaging",color=discord.Color.green())
		.set_author(name='Help Menu | Page 10', icon_url = ctx.author.avatar_url)
		.add_field(name='Magik', value = 'Create some Magik with an image, `magik <image url>`')
		.add_field(name='Deepfry', value = 'Fry some tasty images, `deepfry <image url> <amount of gamma (if left alone 20)>`')
		.add_field(name='Blur', value = 'Blur em to hide sus stuff, `Blur <image url> <amount of gamma (if left alone 20)>`')
		.add_field(name='Avurl', value = 'Convert your avatar into a image compatible with imaging commands, `avurl <user>`')
		.add_field(name='Swirl', value = 'Swirl heh, `swirl <image url> <amount of gamma (if left alone 20)>`')
		.add_field(name='Warp', value = 'Warp an image beyond repair, `warp <image url> <amount of gamma (if left alone 20)>`')
		.add_field(name='Gay', value = 'Feeling like mocking someone? Try this')
		.add_field(name='Glass', value = "Let's try putting some glass in front of an avatar")
		.add_field(name='Invert', value = "Oooo, white. No it's black")
		.add_field(name='Pixelate', value = "BEEP BOOP BOP PIXEL")
		.add_field(name='Greyscale', value = 'Suck all the color out of an avatar')
		.add_field(name='Triggered', value = "I'm Triggereddddd")
		.add_field(name='Color', value = "Get a color with a hex, eg. `color fff`")
		)
		embed1.timestamp = datetime.utcnow()
		embed2.timestamp = datetime.utcnow()
		embed3.timestamp = datetime.utcnow()
		embed4.timestamp = datetime.utcnow()
		embed8.timestamp = datetime.utcnow()
		embed5.timestamp = datetime.utcnow()
		embed7.timestamp = datetime.utcnow()
		embed9.timestamp = datetime.utcnow()
		embed10.timestamp = datetime.utcnow()
		embed11.timestamp = datetime.utcnow()
		featured.timestamp = datetime.utcnow()
		pages = [embed1, embed2, embed3,embed4,embed5,embed7, embed8, embed9,embed10,embed11,featured]
		main = await ctx.send(embed=pages[0])
		await main.add_reaction('⏮')
		await main.add_reaction('⏪')
		await main.add_reaction('⏹')
		await main.add_reaction('⏩')
		await main.add_reaction('⏭')
		current_page = 0
		for i in range(50):
			def check(reaction, user):
				return user == ctx.author
			try:
				reaction, user = await bot.wait_for('reaction_add', check = check, timeout = 10)
				await main.remove_reaction(reaction, user)
				if str(reaction) == '⏮':
					await main.edit(embed=pages[0])
				elif str(reaction) == '⏭':
					await main.edit(embed=pages[len(pages)-1])
					current_page = len(pages)-1
				elif str(reaction) == '⏩':
					page = current_page+1
					current_page = page
					try:
						await main.edit(embed=pages[page])
					except:
						pass
				elif str(reaction) == '⏪':
					page = current_page-1
					current_page = page
					try:
						await main.edit(embed=pages[page])
					except:
						pass
				elif str(reaction) == '⏹':
					current_page = 0
					await main.clear_reactions()

			except asyncio.TimeoutError:
				await main.clear_reactions()
	elif category == "featured":
		await ctx.send(embed=featured)
	elif category in 'anime':
		embed= (discord.Embed(title='Anime', description = 'Find Anime and get watch options\nE.g. `_anime naruto`\n**SubCommands:**\ni) `reviews`\nE.g. `_anime naruto --reviews` ~ Gives a random review\n\nii) `episodes`\nE.g. `_anime naruto --eps/--episodes` ~ Gives the links to first 12 episodes', colour = discord.Color.green()))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'google':
		embed = (discord.Embed(title='Google', description = 'Google anything and get the top 5 results.\n```_google how to get rich?```', colour = discord.Color.green()))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == "dutils" or category == "dankutils":
		embed = (discord.Embed(title = "Dank utilities help",description = "Commands :\n`taxalc` - calcultate dank memer tax\n`fight` - fight as if in dank memer but improved", color = discord.Color.green))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
		
	elif category == "rpg":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Rpg', value = '`maskrpg` and rpg adventure', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "thesis":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Thesis', value = 'type `_thesis` to see all the thesises', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "fun":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Fun', value = '`8ball`, `coolrate`, `simprate`, `gayrate`, `echo`, `flipacoin`, `hug`, `kiss`, `pat`, `slap`, `pp`, `meme`', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "eco" or category == "economy":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Economy', value = '`beg`,`bal`, `bag`, `shop`', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "enc" or category == "encryption":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Encryption', value = 'add e before the following codes to encrypt and d for decrypt eg. `ehex`, `dhex`, `hex`, `base64`, `rot13`, `ascii85`, `base85`', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "mod" or category == "moderator":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Moderator', value = '`lock`, `unlock`, `warn`, `mute`, `unmute`, `kick`, `ban`', inline=False)
		)
		await ctx.send(embed=embed)
	elif category == "utils" or category == "utilities":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Utility', value = '`slowmode`, `avatar`, `gif`, `purge`, `webhook`')
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == "config" or category == "settings":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name = 'Settings', value = '`prefixset`, `muteroleset`')
		)
		await ctx.send(embed=embed)
	elif category == "gaw" or category == "giveaways":
		embed = (discord.Embed(title = 'CereBrus', description = 'One Bot for all Purposes', color= discord.Color.green())
		.add_field(name='Giveaways', value = '`gcreate`,`gend`, `greroll`, `gcancel`', inline=False)
		)
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)
	elif category == '8ball' or category == 'eight ball':
		embed = (discord.Embed(title = '8ball', description = 'Magically get an answer to a question! :8ball:\n```_8ball <question>\n_8ball will i ever get a girlfriend?```', colour = discord.Color.green())
		.set_footer(text='Don\'t take it hard if the reply is not what you expected...'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'coolrate' or category == 'coolr8':
		embed = (discord.Embed(title = 'CoolRate', description = 'Rate how cool you or a mentioned person is! :sunglasses:\n```_coolrate <person/none>\n_coolrate @person\n_coolrate```', colour = discord.Color.green())
		.set_footer(text='Don\'t take it hard if the reply is not what you expected...'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'simprate':
		embed = (discord.Embed(title = 'SimpRate', description = 'Rate how simp you or a mentioned person is! :blush:\n```_simprate <person/none>\n_simprate @person\n_simprate```', colour = discord.Color.green())
		.set_footer(text='Don\'t take it hard if the reply is not what you expected...'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'gayrate' or category == 'howgay':
		embed = (discord.Embed(title = 'GayRate', description = 'Rate how gay you or a mentioned person is! :gay_pride_flag:\nAliases = `howgay`\n```_gayrate|howgay\n_howgay @person```', colour = discord.Color.green())
		.set_footer(text='Don\'t take it hard if the reply is not what you expected...'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'echo' or category == 'say':
		embed = (discord.Embed(title = 'Echo', description = 'Anonymously speak into another channel as the bot!\nAliases = `say`\n```_echo|say <channel> <message>\n_echo #general Wassup Guys i\'m totally Me1iodas```', colour = discord.Color.green())
		.set_footer(text='Use the webhook function to speak as someone else!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'flipacoin' or category == 'tossacoin':
		embed = (discord.Embed(title = 'FlipACoin', description = 'Virtually Toss 1 or a specified number of coins!\n```_flipacoin <number/none>\n_flipacoin 10\n_flipacoin```', colour = discord.Color.green())
		.set_footer(text='More such games coming soon!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'hug' or category == 'kiss' or category == 'pat' or category == 'slap':
		embed = (discord.Embed(title = 'Interactive', description = 'Interact with other users as if IRL using `hug`, `kiss`, `pat`, `slap`\n```_hug/kiss/pat/slap <userid or usermention>\n_hug 750755612505407530 you are my best friend!\n_slap 750755612505407530 dont do that its gross```', colour = discord.Color.green())
		.set_footer(text='Random GIF from Tenor related to the function also adds to the Real-Lifeness [Not NSFW]'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'pp':
		embed = (discord.Embed(title = 'Penis Size', description = 'Get a random size for your penis!\n```_pp <user/none>\n_pp```', colour = discord.Color.green())
		.set_footer(text='NSFW'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'meme':
		embed = (discord.Embed(title = 'Meme', description = 'Get a random, fresh Meme!\n```_meme```', colour = discord.Color.green())
		.set_footer(text='Unlimited Memes Available!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'play' or category == 'p' or category == 'music' or category == 'skip'or category == 'queue' or category == 'pause' or category == 'join' or category == 'leave' or category == 'summon':
		embed = (discord.Embed(title = 'Music', description = 'Listen to Music remotely in any Voice Channel with your Friends!\nCommands include - `play`, `pause`, `stop`, `join`, `summon`, `leave`, `queue`, `skip`, `shuffle`\nAll these serve exactly the functions they speak\n```_play <url/songname>\n_p animals maroon 5```', colour = discord.Color.green())
		.set_footer(text='All Songs Supported!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'slowmode' or category == 'sm':
		embed = (discord.Embed(title = 'Slowmode', description = 'Set the Slowmode for a channel!\n```_slowmode|sm <duration/remove>\n_sm remove\n_sm 2m```', colour = discord.Color.green())
		.set_footer(text='Has permission check!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'purge' or category == 'clear':
		embed = (discord.Embed(title = 'Purge', description = 'Purge is used to clear messages ```_purge <no. of messages>\n_purge 1```', colour = discord.Color.green())
		.set_footer(text='No Limits!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

	elif category == 'webhook':
		embed = (discord.Embed(title = 'Webhook', description = 'Say a message as another user!```_webhook @person <msg>\n_webhook 808609085694935040 hi people i am Nex!!!```', colour = discord.Color.green())
		.set_footer(text='Incredibily Fast!'))
		embed.timestamp = datetime.utcnow()
		await ctx.send(embed=embed)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID'] = 'c1cf58e4dadb4a869f6f114035ce5a18'
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET'] = '745dd988026d4c25ad7debd856a795ce'


def fetch_tracks(sp, item_type, url):
    """
    Fetches tracks from the provided URL.
    :param sp: Spotify client
    :param item_type: Type of item being requested for: album/playlist/track
    :param url: URL of the item
    :return Dictionary of song and artist
    """
    songs_list = []
    offset = 0

    if item_type == 'playlist':
        while True:
            items = sp.playlist_items(playlist_id=url,

                                      fields='items.track.name,items.track.artists(name, uri),'
                                             'items.track.album(name, release_date, total_tracks, images),'

                                             'items.track.track_number,total, next,offset,'
                                             'items.track.id',
                                      additional_types=['track'], offset=offset)
            total_songs = items.get('total')
            for item in items['items']:
                track_name = item['track']['name']
                track_artist = ", ".join([artist['name'] for artist in item['track']['artists']])
                track_album = item['track']['album']['name']
                track_year = item['track']['album']['release_date'][:4]
                album_total = item['track']['album']['total_tracks']
                track_num = item['track']['track_number']
                spotify_id = item['track']['id']
                if len(item['track']['album']['images']) > 0:
                    cover = item['track']['album']['images'][0]['url']
                else:
                    cover = None
            
                if len(sp.artist(artist_id=item['track']['artists'][0]['uri'])['genres']) > 0:
                    genre = sp.artist(artist_id=item['track']['artists'][0]['uri'])['genres'][0]
                else:
                    genre = ""
                songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                                   "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                                   "cover": cover, "genre": genre, "spotify_id": spotify_id})
                offset += 1
                break

    elif item_type == 'album':
        while True:
            album_info = sp.album(album_id=url)
            items = sp.album_tracks(album_id=url)
            total_songs = items.get('total')
            track_album = album_info['name']
            track_year = album_info['release_date'][:4]
            album_total = album_info['total_tracks']
            if len(album_info['images']) > 0:
                cover = album_info['images'][0]['url']
            else:
                cover = None
            if len(sp.artist(artist_id=album_info['artists'][0]['uri'])['genres']) > 0:
                genre = sp.artist(artist_id=album_info['artists'][0]['uri'])['genres'][0]
            else:
                genre = ""
            for item in items['items']:
                track_name = item['name']
                track_artist = ", ".join([artist['name'] for artist in item['artists']])
                track_num = item['track_number']
                spotify_id = item['id']
                songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                                   "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                                   "cover": cover, "genre": genre, "spotify_id": spotify_id})
                offset += 1

    elif item_type == 'track':
        items = sp.track(track_id=url)
        track_name = items['name']
        track_artist = ", ".join([artist['name'] for artist in items['artists']])
        track_album = items['album']['name']
        track_year = items['album']['release_date'][:4]
        album_total = items['album']['total_tracks']
        track_num = items['track_number']
        spotify_id = items['id']
        if len(items['album']['images']) > 0:
            cover = items['album']['images'][0]['url']
        else:
            cover = None
        if len(sp.artist(artist_id=items['artists'][0]['uri'])['genres']) > 0:
            genre = sp.artist(artist_id=items['artists'][0]['uri'])['genres'][0]
        else:
            genre = ""
        songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                           "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                           "cover": cover, "genre": genre, "spotify_id": spotify_id})

    return songs_list

async def search_spotify(type,query):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    songs = fetch_tracks(sp, type, query)
    return songs
