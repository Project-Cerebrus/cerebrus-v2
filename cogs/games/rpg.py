import discord, random
from discord.ext import commands
import os
import subprocess
import asyncio
devs = ['775198018441838642', '750755612505407530', '746904488396324864']
def check4death(health,aihealth):
	if aihealth == 0:
		check4death.death = False
		return check4death.death
	if health == 0:
		check4death.death = True
		return check4death.death
	return
class rpg(commands.Cog, name='RPG'):
	def __init__(self, bot):
		self.bot = bot
	async def stats(self,ctx,health,damage,weapons,defense,author):
		await author.send(f"**Stats:**\nhealth : {health}\ndefense : {defense}\nweapons : {weapons}\n damage : {damage}")
		return
	async def inv(self,ctx,inv):
		for item in inv:
			if item == "apple":
				embed =  (discord.Embed(title="Maskrpg Inventory",description="apple (1)"))
				await ctx.send(embed=embed)
				return
	async def use(self,ctx,inv,item,health):
		if item == "apple":
			health+=5
			return health


	@commands.command()
	async def maskrpg(self,ctx):
		inv = []
		author = ctx.author
		print(author)
		await ctx.send("Start MASK RPG y/n?")
		health = 100
		defense = 0
		weapons = "none"
		damage = 0
		name = ctx.author.name
		try:
				choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
				print(choice.content)
				if choice.content.lower() == "y":
					await ctx.author.send("please read your DMs for the story then answer here, DO NOT TALK ANYWHERE ELSE")
					await asyncio.sleep(1)
					await self.stats(ctx,health,damage,weapons,defense,author)
					await ctx.author.send("You wake up in a dark room and look around, the room is sparse and covered in red paint. There is no furniture or anything standing out besides a door and a box,`check (b)ox or open (d)oor?`")
					try:
						choice2 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
						print(choice2.content)
						if choice2.content.lower() == "b":
							await ctx.author.send("You check the box and find 2 items, an apple and a small pocket knife. You decide to pick the knife and eat the apple. Enter through the door now?(y/n)")
							damage += 5
							inv.append("apple")
							try:
								choice3 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
								print(choice3.content)
								if choice3.content.lower() == "y":
									await ctx.author.send("You go to the door and open it, you see endless darkness. Your vision blacks out, you see a mask stained with blood (Jason the 1st ward) and then you wake up in the same room, there are steps leading down. Go down (y/n)?")
								try:
									choice4 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
									print(choice4.content)
									death = "none"
									if choice4.content.lower() == "y":
										await ctx.author.send("You walk down and find a bloody corpse, what's this? You hear screams. You walk down to find a tall man with hair as black as night staring at you.")
										await ctx.author.send("**Fight Time**")
										await ctx.author.send("Unknown man : What are you doing here?")
										await ctx.author.send("You : What the hell are you doing monster?")
										await ctx.author.send("Unknown man : Just gonna kill you :)")
										await ctx.author.send("type `kick`,`punch` or `heal`")
										aihealth = random.randrange(1,26)
										try:
											choice5 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
											print(choice5.content)
											death = "unknown"
											if choice5.content.lower() == "kick":
												strhealth = str(health)
												luckshot = random.randrange(1,6)
												luckshot2 = random.randrange(1,6)
												damage4fight = damage+luckshot
												aihealth -= damage4fight
												health -= luckshot2
												straihealth = str(aihealth)
												await ctx.author.send(f"You kicked and dealt {damage4fight} to Unknown, he attacked and your health is {strhealth} his health is {straihealth}")
												check4death(health,aihealth)
												if aihealth == 0 or aihealth < 0:
													death = False
												if health == 0 or health < 0:
													death = True
												if death == True:
													await ctx.author.send("You died, most miserably with his knife through your heart, your blood trickling down as you slowly slump over, dead until the next ward.")
												if death == False:
													await ctx.author.send("Unknown : You might have won against me but, it's impossible to win against jason (the 1st ward), my master murders all...")
											if choice5.content.lower() == "punch":
												strhealth = str(health)
												luckshot = random.randrange(1,5)
												luckshot2 = random.randrange(1,5)
												damage4fight = damage+luckshot
												aihealth -= damage4fight
												health -= luckshot2
												straihealth = str(aihealth)
												await ctx.author.send(f"You punch and dealt {damage4fight} to Unknown, he attacked and your health is {strhealth}")
												if aihealth == 0 or aihealth < 0:
													death = False
												if health == 0 or health < 0:
													death = True
												if death == True:
													await ctx.author.send("You died, most miserably with his knife through your heart, your blood trickling down as you slowly slump over, dead until the next ward.")
												if death == False:
													await ctx.author.send("Unknown : You might have won against me but, it's impossible to win against jason (the 1st ward), my master murders all...")
											if choice5.content.lower() == "heal":
												strhealth = str(health)
												luckshot = random.randrange(1,6)
												luckshot2 = random.randrange(1,6)
												healstuff = luckshot
												health += healstuff
												health -= luckshot2
												straihealth = str(aihealth)
												await ctx.author.send(f"You healed {healstuff}, your health is, he attacked and your health is {strhealth} ")
												if death == True:
													await ctx.author.send("You died, most miserably with his knife through your heart, your blood trickling down as you slowly slump over, dead until the next ward.")
												if death == False:
													await ctx.author.send("Unknown : You might have won against me but, it's impossible to win against jason (the 1st ward), my master murders all...")
											while death != False and death != True:
												await ctx.author.send("type `kick`,`punch` or `heal`")
												try:
													choice6 = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
													print(choice6.content)
													death = "unknown"
													if choice6.content.lower() == "kick":
														strhealth = str(health)
														luckshot = random.randrange(1,6)
														luckshot2 = random.randrange(1,6)
														damage4fight = damage+luckshot
														aihealth -= damage4fight
														health -= luckshot2
														straihealth = str(aihealth)
														await ctx.author.send(f"You kicked and dealt {damage4fight} to Unknown, he attacked and your health is {strhealth} his health is {straihealth}")
														check4death(health,aihealth)
														if aihealth == 0 or aihealth < 0:
															death = False
														if health == 0 or health < 0:
															death = True
														if death == True:
															await ctx.author.send("You died")
														if death == False:
															await ctx.author.send("You won")
													if choice6.content.lower() == "punch":
														strhealth = str(health)
														luckshot = random.randrange(1,5)
														luckshot2 = random.randrange(1,5)
														damage4fight = damage+luckshot
														aihealth -= damage4fight
														health -= luckshot2
														straihealth = str(aihealth)
														await ctx.author.send(f"You punch and dealt {damage4fight} to Unknown, he attacked and your health is {strhealth}")
														if aihealth == 0 or aihealth < 0:
															death = False
														if health == 0 or health < 0:
															death = True
														if death == True:
															await ctx.author.send("You died, most miserably with his knife through your heart, your blood trickling down as you slowly slump over, dead until the next ward.")
														if death == False:
															await ctx.author.send("Unknown : You might have won against me but, it's impossible to win against jason (the 1st ward), my master murders all...")
													if choice6.content.lower() == "heal":
														strhealth = str(health)
														luckshot = random.randrange(1,6)
														luckshot2 = random.randrange(1,6)
														healstuff = luckshot
														health += healstuff
														health -= luckshot2
														straihealth = str(aihealth)
														await ctx.author.send(f"You healed {healstuff}, your health is, he attacked and your health is {strhealth} ")
													if death == False:
														await ctx.author.send(f"You slowly walk over to his slumped over body, his pearl white mask glinting in the night... You inspect his inventory and find a small gun. You take it and then continue down. You are faced with two paths, one from which is blood stained and the other is deceptively beautiful, while you walk you stuggle with your memory, all you remember is your name, {name}")
														await asyncio.sleep(1)
														await ctx.author.send("which path will you pick the beautiful one (1) or the second, the blood stained terror (2)")
												except asyncio.TimeoutError:
													await ctx.send("imagine not responding...")
													return
												
										except asyncio.TimeoutError:
											await ctx.send("imagine not responding...")
											return
								except asyncio.TimeoutError:
									await ctx.send("imagine not responding...")
									return
											
								if choice3.content.lower() ==  "n":
									await ctx.author.send("too bad too sad, a cosmic force known as hax forces you to step into the door")
									asyncio.sleep(1)
									await ctx.author.send("fineee you exit the ward and wake up with jason the 7th ward's knife through your skull, your blood slicks down into your eyes. Bye bye :)")
									return
							except asyncio.TimeoutError:
								await ctx.send("imagine not responding...")
						if choice2.content.lower() == "d":
							await ctx.author.send("You go to the door and open it, you see endless darkness. Your vision blacks out, you see a mask stained with blood (Jason the 1st ward) and then you wake up in the same room, there are steps leading down. Go down (y/n)?")
					except asyncio.TimeoutError:
						await ctx.author.send("imagine not responding...")
				if choice.content.lower() == "n":
					await ctx.send("then y tf did u run this cmd lol ~ Devs")
					return
		except asyncio.TimeoutError:
			await ctx.send("imagine not responding...")
			return

	
def setup(bot):
	bot.add_cog(rpg(bot))