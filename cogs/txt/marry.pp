import asyncio
import random

import discord

from discord.ext import commands

#from classes.converters import IntFromTo, MemberWithCharacter, UserWithCharacter

import misc as rpgtools
from checks import has_char
def get_max_kids(self, lovescore):
		return 10 + lovescore // 250_000

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]

class Marriage(commands.Cog):
	def __init__(self, bot):
			self.bot = bot

	
	@commands.command(aliases=["marry"])
	async def propose(self, ctx, partner: discord.Member):
			if partner == ctx.author:
					return await ctx.send("You should have a better friend than only yourself.")
			msg = await ctx.send(
			embed=discord.Embed(
					title=f"{ctx.author} has proposed for a marriage!",
					description=(
							"{author} wants to marry you, {partner}! React with :heart: to marry them!"
					).format(author=ctx.author.mention, partner=partner.mention),
					colour=0xFF0000,
			))
			await msg.add_reaction("\U00002764")

			def reactioncheck(reaction, user):
					return (
							str(reaction.emoji) == "\U00002764"
							and reaction.message.id == msg.id
							and user.id == partner.id
					)

			try:
					reaction, user = await self.bot.wait_for(
							"reaction_add", timeout=120.0, check=reactioncheck
					)
			except asyncio.TimeoutError:
					return await ctx.send("They didn't want to marry.")
			# check if someone married in the meantime
					check1 = await self.bot.pool.fetchrow(
							'SELECT * FROM profile WHERE "user"=$1 AND "marriage"=$2;',
							ctx.author.id,
							0,
					)
					check2 = await self.bot.pool.fetchrow(
							'SELECT * FROM profile WHERE "user"=$1 AND "marriage"=$2;',
							partner.id,
							0,
					)
					if check1 and check2:
							await self.bot.pool.execute(
									'UPDATE profile SET "marriage"=$1 WHERE "user"=$2;',
									partner.id,
									ctx.author.id,
							)
							await self.bot.pool.execute(
									'UPDATE profile SET "marriage"=$1 WHERE "user"=$2;',
									ctx.author.id,
									partner.id,
							)
							await ctx.send(
											"Owwwwwww! :heart: {author} and {partner} are now married!"
									).format(author=ctx.author.mention, partner=partner.mention)
							
					else:
							await ctx.send(
											"Either you or your love married in the meantime... :broken_heart:"
									)
							

	
	@commands.command()
	
	async def divorce(self, ctx):
				
			await self.bot.pool.execute(
					'UPDATE profile SET "marriage"=0 WHERE "user"=$1;', ctx.author.id
			)
			await self.bot.pool.execute(
					'UPDATE profile SET "marriage"=0 WHERE "user"=$1;',
					ctx.character_data["marriage"],
			)
			await self.bot.pool.execute(
					'DELETE FROM children WHERE "father"=$1 OR "mother"=$1;', ctx.author.id
			)
			await ctx.send("You are now divorced.")

	
	@commands.command()
	
	async def relationship(self, ctx):
			partner = await rpgtools.lookup(self.bot, ctx.character_data["marriage"])
			await ctx.send(f"You are currently married to **{partner}**.").format(partner=partner)
			

	
	@commands.command()
	
	async def lovescore(self, ctx, user:discord.Member):
			data = ctx.character_data if user == ctx.author else ctx.user_data
			if data["marriage"]:
					partner = await rpgtools.lookup(self.bot, data["marriage"])
			else:
					partner = ("none")
			await ctx.send(
							"{user}'s overall love score is **{score}**. {user} is married to **{partner}**."
					).format(user=user.name, score=data["lovescore"], partner=partner)
			

	
	@commands.command()
	
	async def spoil(self, ctx, item: int = None):
			items = [
					(("Dog :dog2:"), 50),
					(("Cat :cat2:"), 50),
					(("Cow :cow2:"), 75),
					(("Penguin :penguin:"), 100),
					(("Unicorn :unicorn:"), 1000),
					(("Potato :potato:"), 1),
					(("Sweet potato :sweet_potato:"), 2),
					(("Peach :peach:"), 5),
					(("Ice Cream :ice_cream:"), 10),
					(("Bento Box :bento:"), 50),
					(("Movie Night :ticket:"), 75),
					(("Video Game Night :video_game:"), 10),
					(("Camping Night :fishing_pole_and_fish:"), 15),
					(("Couple Competition :trophy:"), 30),
					(("Concert Night :musical_keyboard:"), 100),
					(("Bicycle :bike:"), 100),
					(("Motorcycle :motorcycle:"), 250),
					(("Car :red_car:"), 300),
					(("Private Jet :airplane:"), 1000),
					(("Space Rocket :rocket:"), 10000),
					(("Credit Card :credit_card:"), 20),
					(("Watch :watch:"), 100),
					(("Phone :iphone:"), 100),
					(("Bed :bed:"), 500),
					(("Home films :projector:"), 750),
					(("Satchel :school_satchel:"), 25),
					(("Purse :purse:"), 30),
					(("Shoes :athletic_shoe:"), 150),
					(("Casual Attire :shirt:"), 200),
					(("Ring :ring:"), 1000),
					(("Balloon :balloon:"), 10),
					(("Flower Bouquet :bouquet:"), 25),
					(("Expensive Chocolates :chocolate_bar:"), 40),
					(("Declaration of Love :love_letter:"), 50),
					(("Key to Heart :key2:"), 100),
					(("Ancient Vase :amphora:"), 15000),
					(("House :house:"), 25000),
					(("Super Computer :computer:"), 50000),
					(("Precious Gemstone Collection :gem:"), 75000),
					(("Planet :earth_americas:"), 1_000_000),
			]
			text = ("Price")
			items_str = "\n".join(
					[
							f"{idx + 1}.) {item} ... {text}: **${price}**"
							for idx, (item, price) in enumerate(items)
					]
			)
			if not item:
					text = (
							"To buy one of these items for your partner, use `{prefix}spoil shopid`"
					).format(prefix=ctx.prefix)
					return await ctx.send(f"{items_str}\n\n{text}")
			item = items[item - 1]
			if ctx.character_data["money"] < item[1]:
					return await ctx.send("You are too poor to buy this.")
			if not ctx.character_data["marriage"]:
					return await ctx.send("You're not married yet.")
					await self.bot.pool.execute(
							'UPDATE profile SET lovescore=lovescore+$1 WHERE "user"=$2;',
							item[1],
							ctx.character_data["marriage"],
					)
					await self.bot.pool.execute(
							'UPDATE profile SET money=money-$1 WHERE "user"=$2;',
							item[1],
							ctx.author.id,
					)
			await ctx.send(
							"You bought a **{item}** for your partner and increased their love score by **{points}** points!"
					).format(item=item[0], points=item[1])
			
			user = await self.bot.get_user_global(ctx.character_data["marriage"])
			if not user:
					return await ctx.send("Failed to DM your spouse, could not find their Discord account")
					
			await user.send((
							"**{author}** bought you a **{item}** and increased your love score by **{points}** points!"
					).format(author=ctx.author, item=item[0], points=item[1])
			)

	
	@commands.command()
	
	#@user_cooldown(43200)
	async def date(self, ctx):
			num = random.randint(1, 15) * 10
			marriage = ctx.character_data["marriage"]
			if not marriage:
					await self.bot.reset_cooldown(ctx)
					return await ctx.send("You are not married yet.")
			await self.bot.pool.execute(
					'UPDATE profile SET lovescore=lovescore+$1 WHERE "user"=$2;', num, marriage
			)

			partner = await self.bot.get_user_global(marriage)
			scenario = random.choice(
					[
							("You and {partner} went on a nice candlelit dinner."),
							("You and {partner} had stargazed all night."),
							("You and {partner} went to a circus that was in town."),
							("You and {partner} went out to see a romantic movie."),
							("You and {partner} went out to get ice cream."),
							("You and {partner} had an anime marathon."),
							("You and {partner} went for a spontaneous hiking trip."),
							("You and {partner} decided to visit Paris."),
							("You and {partner} went ice skating together."),
					]
			).format(partner=(partner.mention if partner else ("Unknown User")))
			text = ("This increased your lovescore by {num}").format(num=num)
			await ctx.send(f"{scenario} {text}")

	'''
	@commands.guild_only()
	@user_cooldown(3600)
	@commands.command(aliases=["fuck", "sex", "breed"])
	
	async def child(self, ctx):
			_("""Make a child with your spouse.""")
			marriage = ctx.character_data["marriage"]
			if not marriage:
					await self.bot.reset_cooldown(ctx)
					return await ctx.send("Can't produce a child alone, can you?")
			async with self.bot.pool.acquire() as self.bot.pool:
					names = await self.bot.pool.fetch(
							'SELECT name FROM children WHERE "mother"=$1 OR "father"=$1;',
							ctx.author.id,
					)
					spouse = await self.bot.pool.fetchval(
							'SELECT lovescore FROM profile WHERE "user"=$1;', marriage
					)
			max_ = self.get_max_kids(ctx.character_data["lovescore"] + spouse)
			if len(names) >= max_:
					await self.bot.reset_cooldown(ctx)
					return await ctx.send(
									"You already have {max_} children. You can increase this limit by increasing your lovescores."
							).format(max_=max_)
					
			names = [name["name"] for name in names]
			user = self.bot.get_user(marriage)
			if not user:
					return await ctx.send("Your spouse is not here.")
			if not await ctx.confirm(
					_("{user}, do you want to make a child with {author}?").format(
							user=user.mention, author=ctx.author.mention
					),
					user=user,
			):
					return await ctx.send("O.o not in the mood today?")

			if random.choice([True, False]):
				ls = random.randint(10, 50)
				await self.bot.pool.execute(
						'UPDATE profile SET "lovescore"="lovescore"+$1 WHERE "user"=$2 OR "user"=$3;',
						ls,
						ctx.author.id,
						marriage,
				)
				return await ctx.send(f"You had a lovely night and gained {ls} lovescore. 😏".format(ls=ls)
			genders = ["m","f"]
			gender = random.choice(genders)
			if gender == "m":
				await ctx.send("It's a boy! Your night of love was successful! Please enter a name for your child.")	
			elif gender == "f":
				await ctx.send("It's a girl! Your night of love was successful! Please enter a name for your child.")
					

			def check(msg):
					return (
							msg.author.id in [ctx.author.id, marriage]
							and 1 <= len(msg.content) <= 20
							and msg.content not in names
							and msg.channel.id == ctx.channel.id
					)

			try:
					msg = await self.bot.wait_for("message", check=check, timeout=30)
			except asyncio.TimeoutError:
				return await ctx.send("You didn't enter a name.")
			name = msg.content.replace("@", "@\u200b")
			async with self.bot.pool.acquire() as self.bot.pool:
					await self.bot.pool.execute(
							'INSERT INTO children ("mother", "father", "name", "age", "gender") VALUES ($1, $2, $3, $4, $5);',
							ctx.author.id,
							marriage,
							name,
							0,
							gender,
					)
			await ctx.send("{name} was born.").format(name=name)
	'''
	'''
	@commands.command()
	
	async def family(self, ctx):
			_("""View your children.""")
			marriage = ctx.character_data["marriage"]
			if not marriage:
					return await ctx.send_("Lonely..."))
			children = await self.bot.pool.fetch(
					'SELECT * FROM children WHERE "mother"=$1 OR "father"=$1;', ctx.author.id
			)
			em = discord.Embed(
					title=_("Your family"),
					description=_("Family of {author} and <@{marriage}>").format(
							author=ctx.author.mention, marriage=marriage
					),
			)
			if not children:
					em.add_field(
							name=_("No children yet"),
							value=_("Use {prefix}child to make one!").format(prefix=ctx.prefix),
					)
			if len(children) <= 5:
					for child in children:
							em.add_field(
									name=child["name"],
									value=_("Gender: {gender}, Age: {age}").format(
											gender=child["gender"], age=child["age"]
									),
									inline=False,
							)
					em.set_thumbnail(url=ctx.author.avatar_url)
					await ctx.sendembed=em)
			else:
					embeds = []
					children_lists = list(chunks(children, 9))
					for small_list in children_lists:
							em = discord.Embed(
									title=_("Your family"),
									description=_("Family of {author} and <@{marriage}>").format(
											author=ctx.author.mention, marriage=marriage
									),
							)
							for child in small_list:
									em.add_field(
											name=child["name"],
											value=_("Gender: {gender}, Age: {age}").format(
													gender=child["gender"], age=child["age"]
											),
											inline=True,
									)
							em.set_footer(
									text=_("Page {cur} of {max}").format(
											cur=children_lists.index(small_list) + 1,
											max=len(children_lists),
									)
							)
							embeds.append(em)
					await self.bot.paginator.Paginator(extras=embeds).paginate(ctx)

	
	@user_cooldown(1800)
	@commands.command(aliases=["fe"])
	
	async def familyevent(self, ctx):
			_("""Events happening to your family.""")
			if not ctx.character_data["marriage"]:
					return await ctx.send_("You're lonely."))
			children = await self.bot.pool.fetch(
					'SELECT * FROM children WHERE "mother"=$1 OR "father"=$1;', ctx.author.id
			)
			if not children:
					return await ctx.send_("You don't have kids yet."))
			target = random.choice(children)
			event = random.choice(
					["death"]
					+ ["age"] * 8
					+ ["namechange"] * 4
					+ ["chest"] * 2
					+ ["moneylose"] * 3
					+ ["moneygain"] * 4
			)
			if event == "death":
					cause = random.choice(
							[
									_("They died because of a shampoo overdose!"),
									_("They died of lovesickness..."),
									_("They've died of age."),
									_("They died of loneliness."),
									_("A horde of goblins got them."),
									_(
											"They have finally decided to move out after all these years, but couldn't survive a second alone."
									),
									_("Spontaneous combustion removed them from existence."),
									_("While exploring the forest, they have gotten lost."),
									_("They've left through a portal into another dimension..."),
									_(
											"The unbearable pain of stepping on a Lego\© brick killed them."
									),  # noqa
									_("You heard a landmine going off nearby..."),
									_("They have been abducted by aliens!"),
									_("The Catholic Church got them..."),
									_("They starved after becoming a communist."),
							]
					)
					await self.bot.pool.execute(
							'DELETE FROM children WHERE "name"=$1 AND ("mother"=$2 OR "father"=$2) AND "age"=$3;',
							target["name"],
							ctx.author.id,
							target["age"],
					)
					return await ctx.send
							_("{name} died at the age of {age}! {cause}").format(
									name=target["name"], age=target["age"], cause=cause
							)
					)
			elif event == "moneylose":
					cause = random.choice(
							[
									_(
											"fell in love with a woman on the internet, but the woman was a man and stole their money."
									),
									_("has been arrested and had to post bail."),
									_("bought fortnite skins with your credit card."),
									_("decided to become communist and gave the money to others."),
									_("bought an inflatable loli."),
									_("was caught pickpocketing and you had to pay the fine."),
									_("gave it to a beggar."),
									_("borrowed it to attend the local knights course."),
									_("spent it in the shop."),
									_("bought some toys."),
									_("has gambling addiction and lost the money..."),
							]
					)
					money = random.randint(0, int(ctx.character_data["money"] / 64))
					await self.bot.pool.execute(
							'UPDATE profile SET "money"="money"-$1 WHERE "user"=$2;',
							money,
							ctx.author.id,
					)

					return await ctx.send
							_("You lost ${money} because {name} {cause}").format(
									money=money, name=target["name"], cause=cause
							)
					)
			elif event == "moneygain":
					cause = random.choice(
							[
									_("finally found a job!"),
									_("won a lottery."),
									_("sold their toys."),
									_("got money from another kid that decided to become communist."),
									_("stole it from a traveller."),
									_("finished a quest with a money reward."),
									_("used dark magic to summon some money."),
									_("looted a local warehouse and sold the wares."),
									_("solved an enigma with a money reward."),
							]
					)
					money = random.randint(1, 5000)
					await self.bot.pool.execute(
							'UPDATE profile SET "money"="money"+$1 WHERE "user"=$2;',
							money,
							ctx.author.id,
					)
					return await ctx.send
							_("{name} gave you ${money}, they {cause}").format(
									name=target["name"], money=money, cause=cause
							)
					)
			elif event == "chest":
					type_ = random.choice(
							["common"] * 500
							+ ["uncommon"] * 200
							+ ["rare"] * 50
							+ ["magic"] * 10
							+ ["legendary"]
					)
					await self.bot.pool.execute(
							f'UPDATE profile SET "crates_{type_}"="crates_{type_}"+1 WHERE "user"=$1;',
							ctx.author.id,
					)
					emoji = getattr(self.bot.cogs["Crates"].emotes, type_)
					return await ctx.send
							_("{name} found a {emoji} {type_} crate for you!").format(
									name=target["name"], emoji=emoji, type_=type_
							)
					)
			elif event == "age":
					await self.bot.pool.execute(
							'UPDATE children SET "age"="age"+1 WHERE "name"=$1 AND ("mother"=$2 OR "father"=$2) AND "age"=$3;',
							target["name"],
							ctx.author.id,
							target["age"],
					)
					return await ctx.send
							_("{name} is now {age} years old.").format(
									name=target["name"], age=target["age"] + 1
							)
					)
			elif event == "namechange":
					await ctx.send
							_("{name} can be renamed! Enter a new name:").format(
									name=target["name"]
							)
					)
					names = [c["name"] for c in children]
					names.remove(target["name"])

					def check(msg):
							return (
									msg.author.id in [ctx.author.id, ctx.character_data["marriage"]]
									and msg.channel.id == ctx.channel.id
									and 0 < len(msg.content) <= 20
									and msg.content not in names
							)

					try:
							msg = await self.bot.wait_for("message", check=check, timeout=30)
					except asyncio.TimeoutError:
							await self.bot.reset_cooldown(ctx)
							return await ctx.send"You didn't enter a name.")
					name = msg.content.replace("@", "@\u200b")
					await self.bot.pool.execute(
							'UPDATE children SET "name"=$1 WHERE "name"=$2 AND ("mother"=$3 OR "father"=$3) AND "age"=$4;',
							name,
							target["name"],
							ctx.author.id,
							target["age"],
					)
					return await ctx.send("{old_name} is now called {new_name}.").format(
									old_name=target["name"], new_name=name
							)
					)

	'''
def setup(bot):
    bot.add_cog(Marriage(bot))
