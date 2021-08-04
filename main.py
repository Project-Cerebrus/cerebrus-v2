from library.funcs import copy_context_with
from colorthief import ColorThief
import os, discord, keep_alive, asyncio, aiohttp, json, requests, random, subprocess, time, traceback, asyncpg, TenGiphPy, pytz,timeago
from discord.ext import commands, slash
from anime_downloader.sites import get_anime_class
from os import listdir
from discord_slash.utils.manage_commands import create_option, create_choice
import tracemalloc
import datetime
#from cerebrus import send_help
#from datetime import datetime
from replit import db
from discord.ext.commands import AutoShardedBot
from dhooks import Webhook
from config import boot
from library import funcs
from cogs.games.economy import get_bank_data
from PIL import Image, ImageFont, ImageDraw
from dotenv import load_dotenv
from cogs.misc.modulus import checkpkg
from discord_slash import SlashCommand
from ChessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from library.whitelist import getlist, add2list
from cogs.fun.marry import mdata
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#pfp_path = "/home/runner/unamed-kacekull/me1iodas.webp"

#fp = open(pfp_path, 'rb')
#pfp = fp.read()
# Data stuffs
changes = "new boot sequence + this lol"

def open_guild(guild):
        guilds = get_guilds_data()
        if str(guild.id) in guilds:
            return False
        else:
            guilds[str(guild.id)] = {}
            guilds[str(guild.id)]["prefix"] = '_'
            guilds[str(guild.id)]["muterole"] = None
            guilds[str(guild.id)]["heistping"] = None
            guilds[str(guild.id)]["heistmanager"] = None
            guilds[str(guild.id)]["auctioneer"] = None

        with open('data/config.json','w') as f:
            json.dump(guilds,f)

        return True
def get_guilds_data():
	with open('data/config.json','r') as f:
		guilds = json.load(f)

	return guilds
guilds = get_guilds_data()
async def determine_prefix(bot, message):
	guild = message.guild
	if str(guild.id) not in guilds or guilds[str(guild.id)]["prefix"] == None:
		default_prefix = '_'
		return default_prefix
	else:
		prefix = guilds[str(guild.id)]["prefix"]
		return prefix
bot = AutoShardedBot(shard_count=10,command_prefix = determine_prefix, case_insensitive = True, intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands = True)

async def dbload(bot):
	#tracemalloc.start()
	bot.pool = await asyncpg.connect("postgres://oaejcblj:evdUZunmgop3DQGaz26UxcB79Dyu0HEU@topsy.db.elephantsql.com:5432/oaejcblj")
	#bot = AutoShardedBot(shard_count=10,command_prefix = determine_prefix, case_insensitive = True, intents = discord.Intents.all(),pool=bot.pool)
	
async def get_servers():
	servers = list(bot.guilds)
	servers = len(servers)
	return servers

bot.owner_ids = [775198018441838642, 746904488396324864, 750755612505407530]
bot.remove_command("help")
bot.avatar = 'https://cdn.discordapp.com/attachments/827040777590538251/841664481058357278/discord-avatar-512-5QS3M.png'
def check_if_it_is_me(ctx):
    return ctx.message.author.id in bot.owner_ids
bot.emotes = {
		"pawn": ["<:pawn_white:798140768379863090>","<:pawn_black:798140768379863060>"],
		"rook": ["<:rook_white:798140768166084609>","<:rook_black:798140768438583296>"],
		"bishop": ["<:bishop_white:798140767801311243>","<:bishop_black:798140768102514699>"],
		"knight": ["<:knight_white:798140768383926272>","<:knight_black:798140768204095508>"],
		"queen": ["<:queen_white:798140768476725278>","<:queen_black:798140768442384404>"],
		"king": ["<:king_white:798140768165429278>","<:king_black:798140768187449395>"]
		}
async def create_connection_pool():
    bot.pg_conn = await asyncpg.create_pool()
def clear():
	os.system("clear")
@bot.event
async def on_ready():
	if boot == "wbhk":
		embed = discord.Embed(title = "Cerebrus",description = f"Cerebrus is back online!",color = discord.Color.green())

		hook = Webhook('https://discord.com/api/webhooks/839764165807177748/cqDNuAsdIKyR0P14YZrRIaS-UcjWcouqVcGUWBQ_Tfufx4lb2yVmKB_SETrn9aZbVyIG')
		
		hook.send(embed=embed)
	try:
		await dbload(bot)
	except:
		print("db load failed")
	print("\n____________________________________________________________________________________________________________")
	print("CereBus Has Started To Torment Souls\nWelcome To Hell!\n From Ace, Kaneki and Skull Crusher...")
	print("\n___________________________	_________________________________________________________________________________")
	await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=f"@Cerebrus"))
	bot.serv_dic = {}
	bot.duel_ids = {}
	bot.spectat_msgs = {}

@slash.slash(name = 'help', 
	description = 'My Help Menu',
	options = [
		create_option(
            name = "category",
            description = "The Category for which you want help.",
            required = False,
            option_type = 3
        )
	]
)
async def _help(ctx, category=None):
	await funcs.send_help(bot,ctx,category)

@slash.slash(name='google', description = 'Get the top 5 results for a search query, straight from Google.',
	options = [
		create_option(name='search_query', description = 'The Query for which I will search Google', required = True, option_type=3)
	])
async def google(ctx, query):
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

@slash.slash(name = 'time', 
	description = 'Get the time for your location.',
	options = [
		create_option(
            name = "timezone",
            description = "The Timezone for which you want the time.",
            required = True,
            option_type = 3
        )
	]
)
async def _time(ctx, timezone=None):
	time_dict = {"ist":"Asia/Kolkata", "cet":"Europe/Africa", "india":"Asia/Kolkata"}
	if timezone.lower() in time_dict:
		timezone = time_dict[timezone]
	try:
		zone = pytz.timezone(timezone)
	except pytz.exceptions.UnknownTimeZoneError:
		return await ctx.send('Unknown Timezone.\nRefer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones', hidden=True)
	time = datetime.now(zone)
	final=f'The Current Time in {timezone} is:\n'+time.strftime('**%-I:%M %p, %d-%b-%Y %Z (UTC%z)**')
	await ctx.send(final, hidden=True)

@slash.slash(name = 'anime', 
	description = 'Get an anime, it\'s watch options, episodes, reviews and more.',
	options = [
		create_option(
            name = "search_query",
            description = "The Tag with which I will search MyAnimeList and fetch results.",
            required = True,
            option_type = 3
        ),
		create_option(
			name='subcommand',
			description = 'Possible SubCommands for the anime like episodes, reviews, etc.',
			required = False,
			option_type=3,
			choices = [
				create_choice(name='episodes', value='episodes'),
				create_choice(name='reviews', value='revs')
			]
		)
	]
)
async def _anime(ctx,search_query:str, subcommand:str=None):
	subtype = subcommand
	print(subtype)
	key = search_query
	main = await ctx.send('Fetching Anime from MyAnimeList...')
	await ctx.channel.trigger_typing()

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

@slash.slash(name = 'gif', 
	description = 'Get a GIF on a particular tag.',
	options = [
		create_option(
            name = "gif_tag",
            description = "The Tag with which i will search.",
            required = True,
            option_type = 3
        )
	]
)
async def gif(ctx, giftag):
	"""This command will return a tenor gif to you"""
	token = "BDE8TTQAN0H1"
	t = TenGiphPy.Tenor(token=token)
	getgifurl = await t.arandom(str(giftag))
	embed = discord.Embed(title = f"Result for '{giftag}' on Tenor", colour = discord.Color.blurple())
	embed.set_image(url = getgifurl)
	await ctx.send(embed=embed)

@slash.slash(name = 'avatar', 
	description = 'View your/someone\'s Avatar',
	options = [
		create_option(
            name = "user",
            description = "The User who's Avatar you want to view.",
            required = False,
            option_type = 6
        )
	]
)
async def avatar(ctx, target:discord.Member=None):
	if target == None:
		target = ctx.author
	avem = discord.Embed(title = f'{str(target)}\'s Avatar',colour=discord.Color.green())
	avem.set_image(url=target.avatar_url)
	avem.timestamp = datetime.datetime.utcnow()
	avem.set_footer(text = f"Requested by {ctx.author.name}", icon_url = ctx.author.avatar_url)
	await ctx.send(embed=avem)

@slash.slash(name = 'info', 
	description = 'View the Bots Real-Time Stats'
)
async def info(ctx):
	servers = await get_servers()
	users = 0
	for guild in bot.guilds:
		users += len(guild.members)
	embed = (discord.Embed(colour = discord.Color.green())
	.add_field(name='Library', value="`discord.py`")
	.add_field(name = 'Users', value = f"`{users}`")
	.add_field(name = 'Servers', value = f"`{servers}`")
	.add_field(name = 'Latency', value = f"`{round(bot.latency*1000)} ms`", inline=False)
	.add_field(name='Developers', value = '<@775198018441838642>: `45%`\n<@746904488396324864>: `45%`\n<@750755612505407530>: `10%`')
	.add_field(name='Prefix', value='`_` (customizable)', inline=False)
	.add_field(name="** **", value = "**[Support Server](https://discord.gg/gm9N3Fr4aV) | [Invite Me](https://discord.com/api/oauth2/authorize?client_id=829241822278058025&permissions=8&scope=bot%20applications.commands)**")
	.set_footer(text= f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
	.set_author(name="Cerebrus Information", icon_url=bot.avatar))
	embed.timestamp = datetime.datetime.utcnow()
	await ctx.send(embed=embed)

@slash.slash(name = 'setnick', 
	description = 'Set a NickName for a User',
	options = [
		create_option(
            name = "user",
            description = "Who's nickname to edit",
            required = True,
            option_type = 6
        ),
		create_option(
            name = "nickname",
            description = "What to change the nick to?",
            required = True,
            option_type = 3
        )
	]
)
async def setnick(ctx, user, new_nick):
	if ctx.author.guild_permissions.manage_users != True:
		return await ctx.send('You don\'t have the permission to use this command.', hidden=True)
	if ctx.author.top_role <= user.top_role:
		return await ctx.send('Can\'t edit Nicknames of people above you.', hidden=True)
	await user.edit(nick=new_nick)
	await ctx.send(f'Edited **{user.name}\'s** Nickname to **{new_nick}**')

@slash.slash(name = 'lock', 
	description = 'Lock the channel for Members',
	options = [
		create_option(
            name = "reason",
            description = "Reason to Lock this Channel",
            required = False,
            option_type = 3
        )
	]
)
async def lock(ctx, reason=None):
	if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True:
		overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = False
		await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		x = reason
		if x == None:
			embed = discord.Embed(title = 'Channel Locked :lock:', description = f'By - {ctx.author.mention} \nReason - None Given', colour = discord.Colour.magenta())
		else:
			embed = discord.Embed(title = 'Channel Locked :lock:', description = f'By - {ctx.author.mention} \nReason - {x}', colour = discord.Colour.magenta())
		await ctx.send(embed=embed)
	else:
		await ctx.send('You don\'t have permissions')

@slash.slash(name = 'unlock', 
	description = 'Unlock the channel for Members',
	options = [
		create_option(
            name = "reason",
            description = "Reason to Unlock this Channel",
            required = False,
            option_type = 3
        )
	]
)
async def unlock(ctx, reason=None):
	if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True:
		overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = True
		await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		x = reason
		if x == None:
			embed = discord.Embed(title = 'Channel Unlocked :unlock:', description = f'By - {ctx.author.mention} \nReason - None Given', colour = discord.Colour.magenta())
		else:
			embed = discord.Embed(title = 'Channel Unlocked :unlock:', description = f'By - {ctx.author.mention} \nReason - {x}', colour = discord.Colour.magenta())
		await ctx.send(embed=embed)
	else:
		await ctx.send('You don\'t have permissions')

@slash.slash(name='purge', 
	description = "Purge messages in the channel",
	options = [
		create_option(
            name = "messages",
            description = "Number of messages to purge",
            required = True,
            option_type = 4
        )
	]
)
async def purge(ctx, messages):
	if ctx.author.guild_permissions.manage_channels != True:
		return await ctx.send('You need the `Manage Channels` permission to do this.')
	await ctx.channel.purge(limit=messages)
	await ctx.send(f"Purged **{messages}** Messages")

@slash.slash(
	name = "choose",
	description = "Choose between upto 5 options!",
	options = [
        create_option(
            name = "option1",
            description = "The 1st Option",
            required = True,
            option_type = 3
        )
        ,create_option(
            name = "option2",
            description = "The 2nd Option",
            required = True,
            option_type = 3
        )
        ,create_option(
            name = "option3",
            description = "The 3rd Option",
            required = False,
            option_type = 3
        )
        ,create_option(
            name = "option4",
            description = "The 4th Option",
            required = False,
            option_type = 3
        )
        ,create_option(
            name = "option5",
            description = "The 5th Option",
            required = False,
            option_type = 3
        )
    ]
)
async def choose(ctx, option1, option2, option3=None, option4=None, option5=None):
	options = [option1, option2, option3, option4, option5]
	for option in options:
		if option == None:
			options.remove(option)
		if '@' in options:
			return await ctx.send('You can\'t mention users/roles.')
		else:
			pass
	options.remove(None)
	ans = random.choice(options)
	options = str(options)
	options = options.replace('[', '')
	options = options.replace(']', '')
	options = options.replace('\'', '')
	embed=discord.Embed(description=f"I Choose... {ans}!", colour = discord.Color.blurple())
	embed.set_author(name = options, icon_url = ctx.author.avatar_url)
	await ctx.send(embed=embed)

@slash.slash(
	name = "ytvc",
	description = "YouTube Together: Voice Activity. Watch YouTube remotely in a VC",
	options = [
        create_option(
            name = "channel",
            description = "Select your desired VC to proceed!",
            required = True,
            option_type = 7
        )
    ]
)
async def ytvc(ctx, channel):
    if str(channel.type) != 'voice':
        return await ctx.send('Channel must be Voice')
    url = f'https://discord.com/api/v8/channels/{channel.id}/invites'
    body = {"max_age": 86400,"max_uses": 0,"target_application_id":"755600276941176913","target_type":2,"temporary":False,"validate":None}
    auth = { "Authorization": "Bot ODI5MjQxODIyMjc4MDU4MDI1.YG1RoA.HJ-oOZKgwr5aUU2l7WyCM8mxGjI", "Content-Type": "application/json", 'X-Ratelimit-Precision': 'millisecond'}

    obj = json.dumps(body, separators=(',', ':'), ensure_ascii=True)
    x = requests.post(url, data = obj, headers = auth)

    string = "https://discord.gg/"
    code = json.loads(x.text)['code']
    invite = string + str(code)
    launch = discord.Embed(colour = discord.Colour.green(), title = "Voice Activity Launched!", description = f"**Link:** [Join]({invite})")
    launch.set_author(name = "Cerebrus", icon_url = bot.avatar)
    launch.add_field(name = "Channel", value = f'```{channel.name}```')
    launch.add_field(name = "Validity", value = "24 hours", inline = False)
    launch.set_footer(text = f"Started By: {str(ctx.author)}", icon_url = ctx.author.avatar_url)
    await ctx.send(embed = launch)

@slash.slash(
	name = "8ball",
	description = "Ask a question for a magical answer!",
	options = [
        create_option(
            name = "question",
            description = "Ask your question!",
            required = True,
            option_type = 3
        )
    ]
)
async def _8ball(ctx, question):
    random_answers = ['No Doubt', 'My sources tell me YES', 'You can rely on that', 'Better not tell you', 'Reply Hazy, Try Again', 'Nah, I wouldn\'t keep my hopes high on that', 'Highly Doubtful', 'Hell No']
    embed=discord.Embed(description=random.choice(random_answers), colour = discord.Color.blurple())
    embed.set_author(name = question, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(
	name = "ping",
	description = "Get the latency of the bot"
)
async def ping(ctx):
	embed = discord.Embed(title="Pong!", description = f"{round(bot.latency*1000)} ms", colour = discord.Color.magenta())
	await ctx.send(embeds=[embed], hidden=True)

@slash.slash(name = 'invite', 
description = 'Invite me to your server!')
async def invite(ctx):
	embed = (discord.Embed(title = 'Invite Me!', description = 'Thanks for choosing me!\n**[Click Me](https://discord.com/api/oauth2/authorize?client_id=829241822278058025&permissions=8&scope=bot%20applications.commands)**\n\n', colour = discord.Color.green())
	.set_footer(text = 'Ty for choosing our bot <3 ~ Devs'))
	await ctx.send(embed=embed)

@bot.event
async def on_shutdown():
	print("shutting cerebrus down...")
	time.sleep(2)
@bot.event
async def on_member_join(meme):
    global last
    last = str(meme.id)
@bot.event
async def on_member_join(member):
    with open('data/users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('data/users.json', 'w') as f:
        json.dump(users, f)




async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('data/levels.json', 'r') as g:
    	levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        #await user.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end
@bot.command(name='user', aliases=['self', 'userstats'])
async def user(ctx, user:discord.Member=None):
	if not user:
		user=ctx.author
	url = user.avatar_url
	r = requests.get(url, allow_redirects=True)
	open('tempimg.gif', 'wb').write(r.content)
	color_thief = ColorThief('tempimg.gif')
	# get the dominant color
	dominant_color = color_thief.get_color(quality=1)
	created_at = user.created_at.strftime('%-d %b %Y')
	joined_at = user.joined_at.strftime('%-d %b %Y')
	now = datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
	main = str(dominant_color).replace('(','').replace(')','').split(", ")
	x = int(main[0])
	y = int(main[1])
	z = int(main[2])

	badges = []
	if r.headers.get('content-type') == "image/gif":
		badges.append("<:nitro:847058195037028382>")
	if user.public_flags.hypesquad_bravery:
		badges.append("<:hypesquad_balance:847052433250713620>")
	if user.public_flags.hypesquad_balance:
		badges.append("<:hypesquad_bravery:847052433116495872>")
	if user.public_flags.hypesquad_brilliance:
		badges.append("<:hypesquad_brilliance:847052433708285963>")
	cretimeago = timeago.format(user.created_at, now)
	jointimeago = timeago.format(user.joined_at, now)
	final1 = str(badges).replace("]","").replace("[","").replace(",","  ").replace("'", "")
	embed = discord.Embed(title=user.name, description = f'{final1}\n\n**Joined Discord on:** {created_at} ({cretimeago})\n**Joined {ctx.guild.name} on:** {joined_at} ({jointimeago})', colour = discord.Color.from_rgb(x,y,z))
	embed.timestamp = datetime.datetime.datetime.utcnow()
	embed.set_thumbnail(url=user.avatar_url)
	await ctx.send(embed=embed)

@bot.command(aliases=["signup","db"])
async def login(ctx):
	with open("data/login/login.json","r") as f:
		loginz = json.load(f)
	if str(ctx.author.name) not in loginz:
		await ctx.send("Check DMs")
		await ctx.author.send("You don't have an account so please type a password you want to use for the login")
		try:
			reply = await bot.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout = 600)
			pwd = str(reply.content)
			loginz[str(ctx.author.name)] = {}
			loginz[str(ctx.author.name)]["password"] = pwd
			loginz[str(ctx.author.name)]["id"] = ctx.author.id
			with open("data/login/login.json","w") as z:
				json.dump(loginz,z)
			await ctx.author.send(f"Username: {ctx.author.name}\nPassword: {pwd}\n*type _login to login*")
			return
		except asyncio.TimeoutError:
			await ctx.send("You didn't respond in time...")
			return
	else:
		if str(ctx.author.id) not in loginz[ctx.author.name]:
			loginz[str(ctx.author.name)]["id"] = ctx.author.id
			with open("data/login/login.json","w") as z:
				json.dump(loginz,z)			
		await ctx.send("https://Cerebus.ace6002.repl.co/login")

@bot.command()
async def setlog(ctx,channel):
	channelid = channel.replace('<#','')
	channelid = channelid.replace('>','')
	#channel = ctx.guild.get_channel(int(channelid))
	with open("data/config.json","r") as f:
		users = json.load(f)
		with open("data/config.json","w") as z:
			users[str(ctx.guild.id)]["logchannel"] = channelid
			json.dump(users,z)

@bot.command()
async def announced(ctx,*,args):
	hook = Webhook('https://discord.com/api/webhooks/839764165807177748/cqDNuAsdIKyR0P14YZrRIaS-UcjWcouqVcGUWBQ_Tfufx4lb2yVmKB_SETrn9aZbVyIG')
	embed = discord.Embed(title = "Cerebrus",description = args,color = discord.Color.green())
	hook.send(embed=embed)
@bot.command(aliases=["rank","levels","profile"])
async def level(ctx, member: discord.Member = None):
	if not member:
			id = ctx.message.author.id
			with open('data/users.json', 'r') as f:
					users = json.load(f)
			lvl = users[str(id)]['level']
			exp = users[str(id)]['experience']
			lvl_end = int(exp ** (1 / 4))
			musers = await mdata()
			eusers = await get_bank_data()
			wallet_amt = eusers[str(id)]["wallet"]
			bank_amt = eusers[str(id)]["bank"]
			partner = musers[str(id)]["partner"]
			embed = (discord.Embed(title = f"{ctx.author.name}'s profile", description = f"**Level**:\nYou are at level {lvl}!\nexperience : {exp}\n **economy**:\nwallet : {wallet_amt}\n bank : {bank_amt}\n net worth : {bank_amt + wallet_amt}\n**Marriage**:\n{partner}",color = discord.Color.green())
			.set_thumbnail(url=ctx.author.avatar_url)
			)
			await ctx.send(embed=embed)
	else:
			id = member.id
			with open('data/users.json', 'r') as f:
					users = json.load(f)
			lvl = users[str(id)]['level']
			exp = users[str(id)]['experience']
			musers = await mdata()
			partner = musers[str(id)]["partner"]
			eusers = await get_bank_data()
			if os.path.isfile('data/vouch.json'):
				with open('data/vouch.json', 'r') as file:
					data = json.loads(file.read())
			if not data:
				data = {}
			vouches = data[str(ctx.guild.id)][str(id)]["Vouches"]["Username"]
			wallet_amt = eusers[str(id)]["wallet"]
			embed = (discord.Embed(title = f"{ctx.author.name}'s level", description = f"You are at level {lvl}!\nexperience : {exp}\n **economy**:\nwallet : {wallet_amt}\n**Vouches**:\n{vouches}",color = discord.Color.green())
			.set_thumbnail(url=member.avatar_url)
			)
			await ctx.send(embed=embed)
@bot.command(name="servers")
async def servers(ctx,action=None):
	await ctx.send("please check terminal (devs only)")
	if action == None:
		for guild in bot.guilds:
			print(guild.name)
			#return
		return

'''@bot.listen('on_message')
async def sneakydeaky(message):
	guild = bot.get_guild(828481893942558720)
	channel = guild.get_channel(844133706481664000)
	if message.author == bot.user:
		return
	await channel.send(f"{message.guild.name} - {message.channel.name}\n{str(message.author)} - {message.content}")'''

@bot.event
async def on_guild_join(guild):
	channel = guild.system_channel
	embed= discord.Embed(title=f'\'Sup {guild.name}! I\'m Cerebrus!', description = 'I am Cerebrus, a multipurpose bot! Aight, I\'ll stop boasting.\nTo ensure that you make full use of my commands, you need to know \'em well.\nUse `_help` for a full, detailed list | `_help <cmd>` for info on a particular command!\nI also have a bunch of Slash Commands, which you may find handy! Just type `/` and wait for it!\nHave some problems? Cerebrus malfunctioning? Found a bug? Make sure to report it in our [Support Server](https://discord.gg/85K38XfG8Q), your 5 minute contribution will help us a lot!\nThanks a bunch for choosing me, see ya!', colour=discord.Color.green())
	embed.timestamp = datetime.datetime.utcnow()
	embed.set_author(name='Cerebrus',icon_url=bot.avatar)
	await channel.send(embed=embed)
	

@bot.command(name='info')
async def info(ctx):
	coms = (len(bot.commands))
	servers = await get_servers()
	users = 0
	for guild in bot.guilds:
		users += len(guild.members)
	def get_guilds_data():
		with open('data/config.json','r') as f:
			guilds = json.load(f)

		return guilds
	guilds = get_guilds_data()
	try:
		prefix = guilds[str(ctx.guild.id)]["prefix"]
	except KeyError:
		prefix = "_"
	embed = (discord.Embed(colour = discord.Color.green())
	.add_field(name='Library', value="`discord.py`")
	.add_field(name = 'Users', value = f"`{users}`")
	.add_field(name = 'Servers', value = f"`{servers}`")
	.add_field(name="Commands", value = f"`{coms}`")
	.add_field(name = 'Latency', value = f"`{round(bot.latency*1000)} ms`", inline=False)
	.add_field(name='Developers', value = '<@775198018441838642>: `45%`\n<@793344086311698442>: `45%`\n<@750755612505407530>: `10%`')
	.add_field(name='Prefix', value=f'`{prefix}` (customizable)', inline=False)
	.add_field(name="** **", value = "**[Support Server](https://discord.gg/gm9N3Fr4aV) | [Invite Me](https://discord.com/api/oauth2/authorize?client_id=829241822278058025&permissions=8&scope=bot%20applications.commands)**")
	.set_footer(text= f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
	.set_author(name="Cerebrus Information", icon_url=bot.avatar))
	embed.timestamp = datetime.datetime.utcnow()
	await ctx.send(embed=embed)

async def game_on(ctx,duel_channel, duelist, victim, duel_msg):
	
	def command_check(message):
		return message.channel == duel_channel and message.author != bot.user
	
	async def endgame():
		await asyncio.sleep(60)
		await duel_channel.delete()
	
	async def get_piece(idt):
		if white == turnset:
			for piece in white_pieces:
				if piece.idt.lower() == idt.lower():
					return piece
			else:
				return None
			
		elif black == turnset:
			for piece in black_pieces:
				if piece.idt.lower() == idt.lower():
					return piece
				
			else:
				return None
	
	board = [[{"color": None, "piece": None} for i in range(8)] for i in range(8)]
	
	# Filling the board's color
	col = "W"
	for line in board:
		for cell in line:
			cell["color"] = col
			
			# Swap the next cell color
			if col == "W":
				col = "B"
			elif col == "B":
				col = "W"
	
	# Filling the board with pieces
	# White Pawns
	for x in range(len(board[1])):
		board[1][x]["piece"] = Pawn("W",x,1,f"P{x+1}")
		
	# Black Pawns
	for x in range(len(board[6])):
		board[6][x]["piece"] = Pawn("B",x,6,f"P{x+1}")
		
	# Rooks
	board[0][0]["piece"] = Rook("W",0,0,"R1")
	board[0][7]["piece"] = Rook("W",7,0,"R2")
	board[7][0]["piece"] = Rook("B",0,7,"R1")
	board[7][7]["piece"] = Rook("B",7,7,"R2")
	
	# Knights
	board[0][1]["piece"] = Knight("W",1,0,"K1")
	board[0][6]["piece"] = Knight("W",6,0,"K2")
	board[7][1]["piece"] = Knight("B",1,7,"K1")
	board[7][6]["piece"] = Knight("B",6,7,"K2")
		
	# Bishops
	board[0][2]["piece"] = Bishop("W",2,0,"B1")
	board[0][5]["piece"] = Bishop("W",5,0,"B2")
	board[7][2]["piece"] = Bishop("B",2,7,"B1")
	board[7][5]["piece"] = Bishop("B",5,7,"B2")
	
	# Queens
	board[0][3]["piece"] = Queen("W",3,0,"Q")
	board[7][3]["piece"] = Queen("B",3,7,"Q")
	
	# Kings
	board[0][4]["piece"] = King("W",4,0,"K")
	white_king = board[0][4]["piece"]
	board[7][4]["piece"] = King("B",4,7,"K")
	black_king = board[7][4]["piece"]
	
	# Randomly decides who is white and who is black
	if random.randint(0,1):
		white = duelist
		black = victim
	
	else:
		white = victim
		black = duelist
	
	# Initialising stuff
	turnset = white
	winner = None		
	old_x = None
	old_y = None
	move_x = None
	move_y = None
	old_piece = None
	castled_rook = False
	white_queen_nb= 1
	black_queen_nb = 1
	white_taken = {"pawn":0,"rook":0,"bishop":0,"knight":0,"queen":0,"king":0}
	black_taken = {"pawn":0,"rook":0,"bishop":0,"knight":0,"queen":0,"king":0}
	
	
	msg = f"Here's how you play chess with {ctx.guild.me.mention}:\n```\n"
	msg += "When it's your turn, move your piece with:  move [piece name] [destination coordinates]\n"
	msg += "For exemple, to move the 3rd Pawn (P3) to the f4 cell, use _move P3 f4\n(note that you can use m instead of move, and that the piece's names and positions aren't caps sensitive)\n\n"
	msg += "Castling is done with castle [castling rook].\nFor exemple, to castle using the R1 rook, use castle R1\n\n"
	msg += "You can concede anytime with concede, even if it's not your turn. You can also ask your opponent to declare the game a draw with draw (they will have to accept).\nTo win, you have to take the king (not just checkmate it)."
	msg += "\n\nWhile I will not register illegal moves, I also won't stop you from putting your king in danger :)\n\n"
	msg += "If someone doesn't take their turn within 10 minutes, the game times out, and the other player is declared winner.\n```"
	await duel_channel.send(msg)
	
	while True:  # Turns will continue until a King is taken
	
		if winner == None:
			
			# Constructing the list of taken pieces as emotes
			white_toadd = ""
			black_toadd = ""
			for taken_piece,nb in white_taken.items():
				if nb == 0:
					continue
				white_toadd += f"  {bot.emotes[taken_piece][1]}\\*{nb}"
			
			for taken_piece,nb in black_taken.items():
				if nb == 0:
					continue
				black_toadd += f"  {bot.emotes[taken_piece][0]}\\*{nb}"
			
			turn_msg = f"**White:** {white.name}  -{white_toadd}\n**Black:** {black.name}  -{black_toadd}"
			
			if old_x != None and old_y != None:
				turn_msg+=f"\nLast turn: **{old_piece.idt}** moved (*{chr(old_x+97)}{old_y+1}* → *{chr(move_x+97)}{move_y+1}*)"
				if castled_rook:
					castled_rook = False
					turn_msg+=" **-castling-**"
			
			turn_msg += f"\nWaiting for a play from: {turnset.mention}"
		else:
			turn_msg = f"**White:** {white.name}\n**Black:** {black.name}\n**{winner.name} WINS!**"
		
		# Checks if either king is in check
		if winner == None:
			white_check = white_king.is_in_check(board)
			black_check = black_king.is_in_check(board)
		
		if white_check[0]:
			turn_msg += "\n**⚠️---THE WHITE KING IS IN CHECK---⚠️**\n"
		if black_check[0]:
			turn_msg += "\n**⚠️---THE BLACK KING IS IN CHECK---⚠️**\n"
		
		# Initalising the list of pieces of both players
		white_pieces = []
		black_pieces = []
		
		# Using PIL to construct the chessboard
		board_img = Image.open("Ressources/ChessBoard.png")
		start_x = 22
		start_y = 1200
		cell_size = 162
		offset = cell_size//4
		
		# Loading the font for the pieces ID
		font = ImageFont.truetype("Ressources/F25_font.ttf", 31)
		draw = ImageDraw.Draw(board_img)
		
		for i in range(8):
			for j in range(8):
				
				# Calculating this cell's absolute coordinates (in px)
				point_coords = (start_x + j*cell_size+offset, start_y- i*cell_size-offset)
				piece = board[i][j]["piece"]
				
				# Skipping empty cells
				if piece == None:
					continue
				else:
					
					# putting the piece into the piece list
					if piece.color == "W":
						white_pieces.append(piece)
					elif piece.color == "B":
						black_pieces.append(piece)
					
					# Getting the corresponding piece file
					piece_filepath = "Ressources/Pieces/"+piece.file
					piece_img = Image.open(piece_filepath)
				
				
				# pasting the piece into the board
				board_img.paste(piece_img,point_coords,piece_img)
				piece_img.close()
				
				# Adding the text
				point_coords = list(point_coords)
				point_coords[0] = point_coords[0] - (offset//3)
				point_coords = tuple(point_coords)
				
				# The text is black, or red if the piece is threatening a king
				color = "black"
				if piece in white_check[1] or piece in black_check[1]:
					color = "red"
				
				draw.text(point_coords,piece.idt,font=font,fill=color)	
		
		# If there was a move last turn, draw a line representing it
		if old_x != None and old_y != None:
			old_px = (start_x+old_x*cell_size+int(2.6*offset),start_y-old_y*cell_size+(offset//1.1))
			new_px = (start_x+move_x*cell_size+int(2.6*offset),start_y-move_y*cell_size+(offset//1.1))
			
			draw.line(old_px + new_px, fill = "red", width=5)
		
		# Saving the image
		randname = random.randint(100,9999999)
		board_img.save(str(randname)+".png")
		board_img.close()
		
		# Sending updated board & updated turn message, then deleting the image
		turn_sent = await duel_channel.send(content=turn_msg, file=discord.File(str(randname)+".png"))
		os.remove(str(randname)+".png")
		
		if winner != None:
			await duel_channel.send(f"{winner.name} wins the game!\n(This channel will be deleted in 1 minute)")
			await endgame()	
			return
		
		end_turn = True
		while True and end_turn:
			
			try:
				reply = await bot.wait_for("message", check=command_check, timeout = 600)
		
			except asyncio.TimeoutError:
				await duel_channel.send(f"{turnset.mention} didn't play in time (10min). Game canceled.\n(This channel will be deleted in 1 minute)")
				await endgame()
				return
			
			
			from_player = reply.author == white or reply.author == black
			if "concede" in reply.content and from_player:
				await duel_channel.send(f"**{reply.author.name} has conceded!**\n(This channel will be deleted in 1 minute)")
				await endgame()
				return
			
			exited_draw = False
			if "draw" == reply.content and from_player:
				bot_msg = await duel_channel.send(f"{reply.author.name} wants to declare this game a draw.\nType `accept` to accept\nType refuse to refuse")
				
				# Waiting for an answer
				while True:
					try:
						reply_draw = await bot.wait_for("message", check=command_check, timeout = 180)
						
					except asyncio.TimeoutError: 
						bot_reply = await duel_channel.send("No reply was given in time. Draw request canceled.")
						exited_draw = True
						break
					
					# The draw request was accepted. Ending the match
					if reply_draw.content == "`accept`":
						await duel_channel.send("**This match has been declared a draw!**\n(This channel will be deleted in 1 minute)")
						await endgame()
						return
					
					elif reply_draw.content == "refuse":
						bot_reply = await duel_channel.send("Draw request refused. The match continues!")
						exited_draw = True
						break
					
					else:
						tmp = await reply_draw.channel.fetch_message(reply_draw.id)
						await tmp.add_reaction("💬")
						await tmp.delete(delay = 15)
			
			# Returns at the start of the loop & cleans the draw message
			if exited_draw:
				await reply.delete(delay = 2)
				await reply_draw.delete(delay = 2)
				await bot_reply.add_reaction("❌")
				await bot_reply.delete(delay = 10)
				await bot_msg.delete(delay = 2)
				
				continue
			
			# If there is no commands, then this is a chat message (15sec lifespan)
			mv_cmd = "move" not in reply.content and "m " not in reply.content
			if mv_cmd and "castle" not in reply.content and "draw" not in reply.content:
				tmp = await reply.channel.fetch_message(reply.id)
				await tmp.add_reaction("💬")
				await tmp.delete(delay = 15)
				continue
			
			if reply.author == turnset:	
				elements = reply.content.split(" ")
				
				# Easy way to avoid problems between commands argument number
				if len(elements)<3:
					elements.append(None)
					elements.append(None)
				
				# Finding the piece in question (if it exists)
				piece = await get_piece(elements[1])
				if piece == None:
					tmp = await reply.channel.fetch_message(reply.id)
					await tmp.add_reaction("👎")
					await tmp.delete(delay =2)
					continue
				
				if "castle" in reply.content:
					
					# Only Rooks can castle
					if type(piece) == Rook:
						king = await get_piece("K")							
						
						# Can't castle if K or R has moved
						if piece.can_castle and king.can_castle:
							castle_check = piece.castling(king.x, king.y, board)
							
							# Can't castle if there's anything in the path
							# Also can't castle if king is in check
							if castle_check[0] and not king.in_check:
								
								# Results depend on the type of castling
								if castle_check[1] == "big":
									k_mod = -2
									r_mod = 3
									
								elif castle_check[1] == "small":
									k_mod = 2
									r_mod = -2
									
								# Moving the Rook
								old_x = piece.x
								old_y = piece.y
								board[piece.y][piece.x+r_mod]["piece"] = piece
								board[old_y][old_x]["piece"] = None
								piece.x = piece.x + r_mod
								piece.can_castle = False
								
								# Moving the king
								old_x = king.x
								old_y = king.y
								board[king.y][king.x+k_mod]["piece"] = king
								board[old_y][old_x]["piece"] = None
								king.x = king.x + k_mod
								king.can_castle = False
								
								# Updates the move coords for the movement line
								move_x = king.x
								move_y = king.y
								old_piece = king
								castled_rook = True
								
								# This turn ends								
								end_turn = False
								continue
										
					# Castling failed
					tmp = await reply.channel.fetch_message(reply.id)
					await tmp.add_reaction("👎")
					await tmp.delete(delay =2)
					continue
								
				
				try:
					move_x = ord(elements[2][0].lower())-97
					move_y = int(elements[2][1])-1
				
				except Exception as e:
					tmp = await reply.channel.fetch_message(reply.id)
					await tmp.add_reaction("👎")
					await tmp.delete(delay =2)
					continue
				
				old_x = piece.x
				old_y = piece.y
				
				# Attempts to move the piece
				if piece.move(move_x, move_y, board):
					
					old_piece = piece
					cur_piece = board[move_y][move_x]["piece"]
					
					if cur_piece != None:
						if turnset == white:
							white_taken[cur_piece.piece_type] += 1
							
						else:
							black_taken[cur_piece.piece_type] += 1
						
					
					# If a king is taken, the game ends
					if board[move_y][move_x]["piece"] != None and board[move_y][move_x]["piece"].idt == "K":
						winner = turnset
					
					board[move_y][move_x]["piece"] = piece
					board[old_y][old_x]["piece"] = None
					
					# If a pawn gets to the end of the board, it becomes a queen
					if "P" in piece.idt and ((piece.y == 0 and piece.color == "B") or (piece.y == 7 and piece.color == "W")):
						
						# Avoids new queens having the same id
						if turnset == white:
							to_add = white_queen_nb
							white_queen_nb +=1
							
						else:
							to_add = black_queen_nb
							black_queen_nb +=1
						
						board[move_y][move_x]["piece"] = Queen(piece.color,piece.x,piece.y,f"Q{to_add}")
						
					
					break
					
				else: 
					tmp = await reply.channel.fetch_message(reply.id)
					await tmp.add_reaction("👎")
					await tmp.delete(delay =2)
					continue
			else:
				tmp = await reply.channel.fetch_message(reply.id)
				await tmp.add_reaction("🤨")
				await tmp.delete(delay =2)
				continue
				
		# Deleting the messages
		tmp = await reply.channel.fetch_message(reply.id)
		await tmp.delete()
		tmp = await turn_sent.channel.fetch_message(turn_sent.id)
		await tmp.delete()
		
		# next turn
		if turnset == white:
			turnset = black
		elif turnset == black:
			turnset = white
		
		end_turn = False
		
		
		
# 
# The _duel command is used to start a game
# 
@bot.command(pass_context=True, aliases = ["game","challenge"])
async def chess(ctx, victim_str=None, *args):
	
	# Called to verify if a message is a reply to a duel request
	def accept_check(message):
		return (message.content == "accept" or message.content == "refuse") and message.author == victim
	
	if ctx.guild == None:
		await ctx.send("You can only use the duel command in a server.")
		return
	
	if not victim_str:
		await ctx.send("You need to specify the user you wish to duel.")
		return
	
	if len(ctx.message.mentions) == 0:
		await ctx.send(f"Cannot find user \"{victim_str.strip('@')}\".")
		return
	
	# The User objects of the 2 participants
	duelist = ctx.author
	victim = ctx.message.mentions[0]
	
	if victim == ctx.author:
		await ctx.send("You can't challenge yourself...")
		return
	
	if victim == bot.user:
		await ctx.send("You cannot challenge me (for your own good).")
		return
	
	await ctx.send(f"{duelist.mention} has challenged you, {victim.mention}, in a game of chess. Will you accept the duel?\n\nType \"`accept`\" to accept the duel.\nType \"`refuse`\" to refuse the duel.")
	
	try:
		reply = await bot.wait_for("message", check=accept_check, timeout = 600)
	
	except asyncio.TimeoutError:
		await ctx.send(f"{duelist.mention}'s challenge request has expired. {victim.mention} didn't accept in time.")
		return
	
	if reply.content == "refuse":
		await ctx.send(f"{victim.mention} has refused {duelist.mention}'s challenge.")
		return
	# If we're here, both parties are ready for the duel
	# Generating duel ID
	duel_id = random.randint(10000, 99999)
	while duel_id in bot.duel_ids.keys():
		duel_id = random.randint(10000, 99999)
		
	bot.duel_ids[duel_id] = ctx.guild.id
	
	# Creating duel channel
	overwrites = {
		ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
		duelist: discord.PermissionOverwrite(read_messages=True, send_messages=True),
		victim:  discord.PermissionOverwrite(read_messages=True, send_messages=True)
		
		}
	
	if "public" in args:
		overwrites[ctx.guild.default_role] = discord.PermissionOverwrite(send_messages=False)
		
	else:
		overwrites[ctx.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
	
	duel_channel = await ctx.guild.create_text_channel(f"chess-{duel_id}", overwrites=overwrites, category=ctx.channel.category)
	
	# Adding duel entry
	if ctx.guild.id not in bot.serv_dic.keys():
		bot.serv_dic[ctx.guild.id] = {}
	
	bot.serv_dic[ctx.guild.id][duel_id] = {
		"duel_channel": duel_channel,
		"duelist": duelist,
		"victim": victim,
		"start_time": datetime.now()
		}
	
	# Sending the duel message
	msg = f"{victim.mention} has accepted {duelist.mention}'s duel!\nThe duel will take place in {duel_channel.mention}."
	if "private" not in args and "public" not in args:
		msg += "\n\n Everyone can react with 👁️ to this message to gain access to the duel channel as a spectator."
	duel_msg = await ctx.send(msg)
	
	# If the game is private, no spectating is allowed
	if "private" not in args and "public" not in args:
		await duel_msg.add_reaction("👁️")
	
		# Storing the message to allow spectators to join
		bot.spectat_msgs[duel_msg.id] = duel_channel
	
	await game_on(ctx, duel_channel, duelist, victim, duel_msg)
	del bot.spectat_msgs[duel_msg.id]
	

@bot.command(pass_context=False)
async def accept(ctx):
	pass
@bot.command(pass_context=False)
async def refuse(ctx):
	pass
@bot.command(pass_context=False)
async def move(ctx):
	pass
@bot.command(pass_context=False)
async def cm(ctx):
	pass
@bot.command(pass_context=False)
async def castle(ctx):
	pass
@bot.command(pass_context=False)
async def draw(ctx):
	pass
@bot.command(pass_context=False)
async def concede(ctx):
	pass



snipe_message_content = None
snipe_message_author = None

@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author
    # Variables outside a function have to be declared as global in order to be changed
    global snipe_msg_avurl
    snipe_message_content = message.content
    snipe_message_author = str(message.author)
    snipe_msg_avurl = message.author.avatar_url
    await asyncio.sleep(60)
    snipe_message_author = None
    snipe_message_content = None
    snipe_msg_avurl = None

@bot.command(name='snipe')
async def snipe(ctx):
	pkg = "snipe"
	check = await checkpkg(ctx.guild.id,pkg)
	if check == "enabled":
		print("[Snipe]: Enabled")
	if check == "disabled":
		await ctx.send("command disabled, use mpkg to reinstall")
		return
	if snipe_message_content==None:
		await ctx.reply("There's nothing to snipe.")
	else:
		embed = discord.Embed( description=f"{snipe_message_content}")
		embed.set_author(name=snipe_message_author, icon_url = snipe_msg_avurl)
		embed.set_footer(text=f"Sniped by {ctx.author.name}#{ctx.author.discriminator}")
		await ctx.send(embed=embed)
		return

@bot.command(aliases=['jailbreak', 'quarantine',"jisheku"])
async def jailshell(ctx,*,pwd):
	if pwd == "jailiskool":
		await ctx.message.delete()
		await ctx.send("Entering jailshell...\nNote: There won't be a confirmation message for this.")
		os.system("python jailshell.py")
	elif pwd != "jailiskool":
		await ctx.send("sup imposter logging your details... ~ Kaneki")
		autheval = str(ctx.author.id)
		f = open("jaillog.txt", "a")
		f.write("\n" +  "<@" + autheval + ">" + " : " + pwd)
		f.close()
for file in listdir('cogs/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
for file in listdir('cogs/config/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.config.{file[:-3]}')
for file in listdir('cogs/fun/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.fun.{file[:-3]}')
for file in listdir('cogs/games/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.games.{file[:-3]}')
for file in listdir('cogs/utility/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.utility.{file[:-3]}')
for file in listdir('cogs/misc/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.misc.{file[:-3]}')
bot.load_extension('jishaku')

@bot.command(name='help', aliases=['commands'])
async def __help(ctx, *, category=None):
	await funcs.send_help(bot, ctx, category)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(error)
	elif isinstance(error, commands.CommandOnCooldown):
			error_list = ['Woah, slow down there Sheriff!','Too fast for me, let me breath!','Spamming isn\'t cool!','Im too lazy!','Later, Aligator!','Take it slow there buddy!']
			error_random = random.choice(error_list)
			
			error_embed = discord.Embed(title = f"{error_random}", description = "You're going too fast!\nThis Command is on Cooldown!\nWait **{:.0f} seconds** until the cooldown is over!".format(error.retry_after), color = discord.Color.green())
			error_embed.set_footer(text = "Cerebrus Premium: Coming Soon!")
			return await ctx.send(embed = error_embed)
	elif isinstance(error, commands.CommandNotFound):
		embed = discord.Embed(title='Command not Found!', description = f"{error}\nUse `_help` for a list of my commands!", color = discord.Color.green())
		return await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title='Missing Permissions!', description = f"{error}", color = discord.Color.green())
		return await ctx.send(embed=embed)
	else:
		raise error

@bot.listen('on_message')
async def reply_to_mention(msg):
	open_guild(msg.guild)
	guilds = get_guilds_data()
	guild = msg.guild
	prefix = guilds[str(guild.id)]["prefix"]
	if prefix == None:
			prefix = '_'
	if msg.mentions != []:
			if msg.mentions[0] == bot.user:
					embed = (discord.Embed(title = f"Hello {msg.author.name}!\nI am Cerebrus, a Multipurpose Bot!", description = f'My Prefix for this server is `{prefix}`!\nUse `{prefix}help` to get started!', colour = discord.Color.green())
					.set_footer(text = f'Use {prefix}invite to invite me!'))
					xd = await msg.channel.send(embed=embed)
					await asyncio.sleep(10)
					await xd.delete()
'''
@bot.listen('on_message')
async def reply_to_afk(message):
    user = message.author
    def get_afk_data():
        with open("data/afk.json", "r") as f:
            users = json.load(f)
            return users

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
    open_afk(user)
    try:
        user = message.author
        users = get_afk_data()
        open_afk(user)
    except KeyError:
        if users[str(user.id)]["afk_status"] == True:
            users[str(user.id)]["afk_status"] = False
            users[str(user.id)]["afk_msg"] = None
            with open("afk.json", "w") as f:
                json.dump(users, f)
            embed = (discord.Embed(title = f"{str(user)} is no longer AFK", colour = discord.Color.magenta())
            .set_thumbnail(url=user.avatar_url))
            embed.timestamp = datetime.datetime.utcnow()
            x = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await x.delete()
        if len(message.mentions) != 0:
            user = message.mentions[0]
            users = get_afk_data()
            open_afk(user)
            x = users[str(user.id)]["afk_status"]
            if x == False:
                return

            else:
              	if message.author.id != user.id:
                    y = users[str(user.id)]["afk_msg"]
                    embed = (discord.Embed(title = f"{str(user)} is AFK", description = y, colour = discord.Color.magenta())
                    .set_thumbnail(url = user.avatar_url))
                    x = await message.channel.send(embed=embed)
                    await asyncio.sleep(5)
                    await x.delete()
    finally:
        if users[str(user.id)]["afk_status"] == True:
            users[str(user.id)]["afk_status"] = False
            users[str(user.id)]["afk_msg"] = None
            with open("data/afk.json", "w") as f:
                json.dump(users, f)
            embed = (discord.Embed(title = f"{str(user)} is no longer AFK", colour = discord.Color.magenta())
            .set_thumbnail(url=user.avatar_url))
            embed.timestamp = datetime.datetime.datetime.utcnow()
            x = await message.channel.send(embed=embed)
            await asyncio.sleep(5)
            await x.delete()
        if len(message.mentions) != 0:
            user = message.mentions[0]
            users = get_afk_data()
            open_afk(user)
            x = users[str(user.id)]["afk_status"]
            if x == False:
                pass
            if message.author.id != user.id:
                    y = users[str(user.id)]["afk_msg"]
                    embed = (discord.Embed(title = f"{str(user)} is AFK", description = y, colour = discord.Color.magenta())
                    .set_thumbnail(url = user.avatar_url))
                    x = await message.channel.send(embed=embed)
                    await asyncio.sleep(5)
                    await x.delete()
'''
@bot.listen('on_message')
async def abc(message):
	if message.channel.name == "c-abc":
		if message.author.bot:
			return
		with open("data/abc.json","r") as f:
			ab = json.load(f)
		if str(message.guild.id) not in ab:
			ab[str(message.guild.id)] = {}
			ab[str(message.guild.id)]["letters"] = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","w","v","x","y","z"]
			ab[str(message.guild.id)]["on"] = 0
			with open("data/abc.json","w") as z:
				json.dump(ab,z)
		letters = ab[str(message.guild.id)]["letters"]
		on = ab[str(message.guild.id)]["on"] 
		if message.content == (letters[on]):
				await message.add_reaction("👍")
				if letters[on] == "z":
					ab[str(message.guild.id)]["on"] = 0
					await message.channel.send("Back to `a`")
				else:
					ab[str(message.guild.id)]["on"] += 1
				with open("data/abc.json","w") as z:
					json.dump(ab,z)

		else:
			if message.author.bot:
				return
			ab[str(message.guild.id)]["on"] = 0
			with open("data/abc.json","w") as z:
				json.dump(ab,z)
			return await message.channel.send(f"Wrong word it was `{letters[on]}`\nback to `a`")
			
@bot.listen('on_message')
async def count(message):
	if message.channel.name == "c-count":
		if message.author.bot:
			return
		with open("data/count.json","r") as f:
			ab = json.load(f)
		if str(message.guild.id) not in ab:
			ab[str(message.guild.id)] = 0
			with open("data/count.json","w") as z:
				json.dump(ab,z)
		number = ab[str(message.guild.id)]
		if message.content == (str(number)):
				await message.add_reaction("👍")
				ab[str(message.guild.id)] += 1
				with open("data/count.json","w") as z:
					json.dump(ab,z)

		else:
				if message.author.bot:
					return
				ab[str(message.guild.id)] = 0
				with open("data/count.json","w") as z:
					json.dump(ab,z)
				return await message.channel.send(f"Wrong number it was `{number}`\nback to `0`")

@bot.listen('on_message')
async def sticky(message):
	if message.author.bot:
		return
	with open("data/sticky.json","r") as f:
		st = json.load(f)
	if str(message.channel.id) in st:
		msg = st[str(message.channel.id)]
		await message.channel.send(msg)

keep_alive.keep_alive()
bot.run("")
