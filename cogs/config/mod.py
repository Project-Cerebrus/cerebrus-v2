devs = ['775198018441838642', '750755612505407530', '746904488396324864']
import discord, random, asyncio, difflib, json
from difflib import get_close_matches
from discord.ext import commands
from library.whitelist import checklist
verifyrole = []
memberrole = []
async def open_guild(guild):

	guilds = await get_guilds_data()

	if str(guild.id) in guilds:
		return False
	else:
		guilds[str(guild.id)] = {}
		guilds[str(guild.id)]["prefix"] = None
		guilds[str(guild.id)]["muterole"] = None
		guilds[str(guild.id)]["heistping"] = None
		guilds[str(guild.id)]["heistmanager"] = None
		guilds[str(guild.id)]["auctioneer"] = None

	with open('data/config.json','w') as f:
		json.dump(guilds,f)

	return True


async def get_guilds_data():
	with open('data/config.json','r') as f:
		guilds = json.load(f)

	return guilds

async def open_lock(guild):

	guilds = await get_lock_data()

	if str(guild.id) in guilds:
		return False
	else:
		guilds[str(guild.id)] = {}
		guilds[str(guild.id)]["channels"] = []

	with open('data/tolock.json','w') as f:
		json.dump(guilds,f)

	return True


async def get_lock_data():
	with open('data/tolock.json','r') as f:
		guilds = json.load(f)

	return guilds

class moderator(commands.Cog, name='Moderator'):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases=["fn"])
	async def freezenick(self,ctx,user:discord.Member,nick,timer):
		timer = int(timer)
		while timer > 0 or timer != 0:
			await user.edit(nick=nick)
			await asyncio.sleep(1)
			timer -= 1
	
	@commands.command(name='lock', brief = 'Locks the channel', description = 'Locks down the channel for the default role', aliases = ['lk', 'l'])
	async def lock(self, ctx, *, reason=None):
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

		elif str(ctx.author.id) == devs:
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
			await ctx.reply('You dont have permissions')

	@commands.command(name='unlock', brief = 'Unlocks a channel', description = 'Unlocks the channel for the default role', aliases = ['unlk', 'ul'])
	async def unlock(self, ctx, *, reason=None):
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
			await ctx.reply('You dont have permissions')

	@commands.command(name='nuke')
	@commands.has_permissions(manage_channels=True)
	async def nuke(self, ctx):
		channel = ctx.channel
		position = channel.position
		x = await channel.clone()
		await x.edit(position = position)
		await channel.delete()

		msg=await x.send(f'Nuked! {channel.name}')
		msg=await x.send('Nuked!')
		await asyncio.sleep(5)
		await msg.delete()

	@commands.command(name = 'lockdown')
	@commands.has_permissions(manage_channels=True)
	async def lockdown(self, ctx, *, args=None):
		locks = await get_lock_data()
		guild = ctx.guild
		if locks[str(guild.id)]["status"] == "locked":
			return await ctx.reply("We are already locked up.\nRun `_unlockdown` to revert this.")
		channels = locks[str(guild.id)]["channels"]
		await ctx.channel.trigger_typing()
		for channel in channels:
			channel = ctx.guild.get_channel(int(channel))
			if str(channel.type) == 'text' and channel != ctx.channel:
				overwrite = channel.overwrites_for(ctx.guild.default_role)
				overwrite.send_messages = False
				await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
				embed = discord.Embed(title = 'Server Lockdown :lock:', description = f'By - {ctx.author.mention} \nReason - {args}', colour = discord.Colour.magenta())
				await channel.send(embed=embed)
				await asyncio.sleep(2)
		locks[str(guild.id)]["status"] = "locked"
		with open('data/tolock.json','w') as f:
			json.dump(locks,f)
		await ctx.send('Locked Up the Server.')

	@commands.command(name = 'unlockdown')
	@commands.has_permissions(manage_channels=True)
	async def unlockdown(self, ctx, *, args=None):
		locks = await get_lock_data()
		guild = ctx.guild
		if locks[str(guild.id)]["status"] == "unlocked":
			return await ctx.reply("We are already unlocked.\nRun `_lockdown` to lock the server.")
		channels = locks[str(guild.id)]["channels"]
		await ctx.channel.trigger_typing()
		for channel in channels:
			channel = ctx.guild.get_channel(int(channel))
			await asyncio.sleep(0.25)
			if str(channel.type) == 'text' and channel != ctx.channel:
				overwrite = channel.overwrites_for(ctx.guild.default_role)
				overwrite.send_messages = True
				await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
				embed = discord.Embed(title = 'Server Unlockdown :unlock:', description = f'By - {ctx.author.mention} \nReason - {args}', colour = discord.Colour.magenta())
				await channel.send(embed=embed)
				await asyncio.sleep(2)
		locks[str(guild.id)]["status"] = "unlocked"
		with open('data/tolock.json','w') as f:
			json.dump(locks,f)
		await ctx.send('Unlocked the Server.')

	global found
	found = False
	@commands.command(name = 'roleall')
	async def roleall(self, ctx, role:str):
		for r in ctx.guild.roles:
			if str(role) in str(r).lower():
				toadd = r
			else:
				return await ctx.send(f'Role {role} not found.')
		await ctx.send(f'Beginning to add **{toadd.name}** to **{len(ctx.guild.members)} Members**')
		await ctx.channel.trigger_typing()
		for member in ctx.guild.members():
			await member.add_roles(toadd)
		await ctx.send(f'Added **{toadd.name}** to **{len(ctx.guild.members)} Members**')
	@commands.command(name='role', brief = 'Add/Remove a role', description = 'If the person has the role, it removes it. If they don\'t then it adds it', aliases = ['r'])
	@commands.has_permissions(manage_roles=True)
	async def role(self, ctx, member:discord.Member=None, *, role: str=None):
		role = role.lower()
		if member == None or role == None:
			await ctx.reply('**Syntax Error:**\n```Use _role @member rolename```')
			return
		found = False
		for r in ctx.guild.roles:
			if str(role) in str(r).lower():
				found = True
				if ctx.author.top_role.position <= r.position and ctx.author.id not in devs:
					await ctx.reply('Nice try...\nYou can\'t add this role as it is higher than your highest role.')
					return
				else:
					if r in member.roles:
						await member.remove_roles(r)
						await ctx.reply(f'Removed **{r.name}** from **{str(member)}**')
						break
					else:
						await member.add_roles(r)
						await ctx.reply(f'Added **{r.name}** to **{str(member)}**')
						break

		if found != True:
			await ctx.reply("Please type a valid role.")

	@commands.command(name='editrole', brief = 'Add/Remove a role', description = 'If the person has the role, it removes it. If they don\'t then it adds it', aliases = ['edit role'])
	@commands.has_permissions(manage_roles=True)
	async def editrole(self, ctx, action=None, *, role: str=None):
		role = role.lower()
		if action == 'position':
			if role == None:
				await ctx.reply('**Syntax Error:**\n```Use _editrole position rolename```')
				return
			found = False
			
			for r in ctx.guild.roles:
				if str(role) in str(r).lower():
					found = True
					if int(ctx.author.top_role.position) <= int(r.position):
						await ctx.reply('Nice try...\nYou can\'t move this role as it is higher/same as your highest role.')
						return
					else:
						await ctx.send(f'Which Position would you like to move **{r.name}** to?')
						pos = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)
						pos = int(pos.content)
						await r.edit(position = int(pos))
						await ctx.send(f'Moved **{r.name}**')
			if found != True:
				await ctx.reply("Please type a valid role.")

		elif action == 'color':
			if role == None:
				await ctx.reply('**Syntax Error:**\n```Use _editrole color rolename```')
				return
			found = False
			for r in ctx.guild.roles:
				if str(role) in str(r).lower():
					found = True
					if int(ctx.author.top_role.position) <= int(r.position):
						await ctx.reply('Nice try...\nYou can\'t edit this role as it is higher/same as your highest role.')
						return
					else:
						await ctx.send(f'Which Color would you like to add to **{r.name}**?')
						pos = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)
						if '#' in pos.content:
							pos.content = pos.content.strip('#')
						pos2 = pos.content
						pos = int(pos.content, base=16)
						await r.edit(colour = discord.Color(value = pos))
						await ctx.send(f'Added Color **#{pos2}** to **{r.name}**')
			if found != True:
				await ctx.reply("Please type a valid role.")

		elif action == 'name':
			if role == None:
				await ctx.reply('**Syntax Error:**\n```Use _editrole name rolename```')
				return
			found = False
			for r in ctx.guild.roles:
				if str(role) in str(r).lower():
					found = True
					if int(ctx.author.top_role.position) <= int(r.position):
						await ctx.reply('Nice try...\nYou can\'t edit this role as it is higher/same as your highest role.')
						return
					else:
						await ctx.send(f'Which would you like the new name of **{r.name}** to be?')
						prevr = r.name
						pos = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)
						await r.edit(name = pos.content)
						await ctx.send(f'Changed **{prevr}**\'s name to **{pos.content}**')
			if found != True:
				await ctx.reply("Please type a valid role.")

		else:
			await ctx.reply('Please provide a valid action\n```_editrole position <rolename>\n_editrole color <rolename>\n_editrole name <rolename>```')


	@commands.command(name = 'warn', brief = 'Warns Someone', aliases = ['w'])
	@commands.has_permissions(manage_guild=True)
	async def warn(self, ctx, user:discord.Member=None, *, reason=None):
		if user == None:
			await ctx.reply('You haven\'t mentioned anyone to warn...\nDoes that mean you want me to warn you?')
			return
		if ctx.author.top_role < user.top_role:
			await ctx.reply('**Action Aborted**\nReason - This person is higher than you in the role hierarchy.')
			return
		with open("data/mod.json", "r") as f:
			users = json.load(f)

		def open_mod(user):
			with open("data/mod.json", "r") as f:
				users = json.load(f)
			if str(user.id) in users:
				return False
			else:
				users[str(user.id)] = {}
				users[str(user.id)]["warns"] = None
			with open("data/mod.json", "w") as f:
				json.dump(users, f)
			return True
		open_mod(user)
		if users[str(user.id)]["warns"] == None:
			users[str(user.id)]["warns"] = [str(reason)]
		else:
			l1 = users[str(user.id)]["warns"]
			users[str(user.id)]["warns"] = l1.append(str(reason))
		with open("data/mod.json", "w") as f:
			json.dump(users, f)
		await ctx.reply(f'Warned **{user.name}** for **{reason}**')
		await user.send(f'You were warned in **{ctx.guild.name}** for **{reason}**')
	@commands.command()
	async def verify(self,ctx):
		alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
		l1 = random.choice(alpha)
		l2 = random.choice(alpha)
		l3 = random.choice(alpha)
		l4 = random.choice(alpha)
		await ctx.author.send(f"type the following code in\n`{l1}{l2}{l3}{l4}`")
		code = l1 + l2 + l3 + l4
		print(code)
		choice = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
		print(choice.content)
		if choice.content.lower() == code:
			user = ctx.message.author
			
			try:
				role = discord.utils.get(user.server.roles, name="not verified")
				role2 = discord.utils.get(user.server.roles, name="member")
				role3 = discord.utils.get(user.server.roles, name="verified")
				await self.bot.remove_roles(user, role)
				await self.bot.add_roles(user, role2)
				await self.bot.add_roles(user, role3)
			except:
				await ctx.author.send("Failed verify:\nplease contact a moderator to create a role called `not verified` and a role called `verified` or `member`")
		if choice.content.lower() != code:
			await ctx.author.send("You failed verification please rerun the command")
	@commands.command(pass_context=True,name='mute', brief = 'Mutes Someone', description = 'Adds the muted role to the mentioned user', aliases = ['mu'])
	async def mute(self, ctx, member:discord.Member=None, *, reason=None):
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		muterolen = guilds[str(guild.id)]["muterole"]
		if muterolen == None:
			return await ctx.reply('MuteRole not Configured.\nUse `_setm <roleid/rolemention>` to configure it.')
		muterole = ctx.guild.get_role(int(muterolen))
		if member == None:
			await ctx.reply('Can\'t mute no one')
			return
		if ctx.author.top_role < member.top_role:
			await ctx.reply('You can only mute Members below you.')
			return
		await member.add_roles(muterole)
		await ctx.reply(f'Muted **{member.name}** with reason **{reason}**')
		await member.send(f'You were Muted in **{ctx.guild.name}** for reason: **{reason}**')
		return
	@commands.command(pass_context=True,name='hardmute', brief = 'Mutes Someone', description = 'Adds the muted role to the mentioned user', aliases = ['hm'])
	async def hardmute(self, ctx, member:discord.Member=None, *, reason=None):
		prevrole = []
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		muterolen = guilds[str(guild.id)]["muterole"]
		if muterolen == None:
			return await ctx.reply('MuteRole not Configured.\nUse `_setm <roleid/rolemention>` to configure it.')
		muterole = ctx.guild.get_role(int(muterolen))
		if member == None:
			await ctx.reply('Can\'t mute no one')
			return
		if ctx.author.top_role < member.top_role:
			await ctx.reply('You can only mute Members below you.')
			return
		await ctx.reply(f'Hardmuted **{member.name}** with reason **{reason}**')
		await member.send(f'You were hardmuted in **{ctx.guild.name}** for reason: **{reason}**')
		for role in member.roles:
			role2 = discord.utils.find(lambda r: r.name == role, ctx.message.guild.roles)
			prevrole.append(role2)
			await member.remove_roles(role2)
			await member.add_roles(muterole)
		asyncio.sleep(5)
		for prevroles in prevrole:
			await member.add_roles(prevrole)
		return
	@commands.command(pass_context=True,name='tempmute', aliases = ['tm'])
	async def tempmute(self, ctx, member:discord.Member=None, no_time=None, *, reason=None):
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		muterolen = guilds[str(guild.id)]["muterole"]
		if muterolen == None:
			return await ctx.reply('MuteRole not Configured.\nUse `_setm <roleid/rolemention>` to configure it.')
		muterole = ctx.guild.get_role(int(muterolen))
		if member == None:
			await ctx.reply('Can\'t mute no one')
			return
		if ctx.author.top_role < member.top_role:
			await ctx.reply('You can only mute Members below you.')
			return
		await member.add_roles(muterole)
		if 's' in no_time:
			t = no_time.strip('s')
			t = int(t)
			f_time = int(t)

		elif 'h' in no_time:
			t = no_time.strip('h')
			t = int(t)
			f_time = int(t * 3600)

		elif 'm' in no_time:
			t = no_time.strip('m')
			t = int(t)
			f_time = int(t * 60)
		await ctx.reply(f'Muted **{member.name}** for {no_time} with reason **{reason}**')
		await member.send(f'You were Muted in **{ctx.guild.name}** for {no_time} with reason: **{reason}**')
		await asyncio.sleep(f_time)
		if muterole not in member.roles:
			return await ctx.send(f'{member.name} was already unmuted.')
		await member.remove_roles(muterole)
		await ctx.send(f'Unmuted {member.mention} after {no_time}')

	@commands.command(name='unmute', brief = 'Unmutes a muted person', description = 'Unmutes a mentioned person.', aliases = ['um'])
	async def unmute(self, ctx, user:discord.Member=None):
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		muterolen = guilds[str(guild.id)]["muterole"]
		if muterolen == None:
			return await ctx.reply('MuteRole not Configured.\nUse `_setm <roleid/rolemention>` to configure it.')
		muterole = ctx.guild.get_role(int(muterolen))
		if user == None:
			await ctx.reply('Mention a muted person to unmute.')
			return
		if muterole not in user.roles:
			await ctx.reply('This Person is not Muted.')
			return
		if ctx.author.top_role < user.top_role:
			await ctx.reply('Can only unmute people below you.')
			return
		await user.remove_roles(muterole)
		await ctx.send(f'Unmuted **{user.name}**')

	@commands.command(name='kick', brief = 'Kicks a mentioned person.', description = 'Kicks a person in the server [must be lower than you]', aliases = ['k'])
	@commands.has_permissions(ban_members=True)
	async def kick(self, ctx, person:discord.Member=None, *, reason=None):
		if person == None:
			await ctx.send('Can\'t kick no one')
			return
		if ctx.author.top_role < person.top_role:
			await ctx.reply('Cannot do this action due to role hierarchy.\nThis person is higher than you.')
			return
		try:
			await ctx.guild.kick(person, reason=reason)
			embed=discord.Embed(title = f"Kicked {person.name}", description = f'Reason - {reason}\nModerator: {ctx.author.name}', colour=discord.Color.red())
			embed.set_thumbnail(url = person.avatar_url)
			await ctx.send(embed=embed)
		except:
			await ctx.reply('**Error:**\nThis user is higher than me in the role hierarchy.')
			return

	@commands.command(name='ban', brief = 'Bans a person', description = 'Bans a mentioned person [must be lower than you in the hierarchy]', aliases = ['b', 'hammer'])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, person:discord.Member=None, *, reason=None):
		if person == None or person == ctx.author:
			await ctx.reply('Can\'t ban no one')
			return
		if ctx.author.top_role < person.top_role:
			await ctx.reply('Cannot do this action due to role hierarchy.\nThis person is higher than you.')
			return
		else:
			try:
				await ctx.guild.ban(person, reason=reason)
				embed=discord.Embed(title = f"Banned {person.name}", description = f'Reason - {reason}\nModerator: {ctx.author.name}', colour=discord.Color.red())
				embed.set_thumbnail(url = person.avatar_url)
				await ctx.send(embed=embed)
			except:
				await ctx.reply('**Error:**\nThis user is higher than me in the role hierarchy.')
				return

	@commands.command(name = 'unban', aliases = ['ub'])
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, user,*, reason=None):
		'''bans = await ctx.guild.bans()'''
		try:
			int(user)
		except:
			await ctx.reply('Failed to Convert User into Integer')
			pass
		'''for entry in bans:
			person = entry.user
			if user in str(person.name).lower() or user in str(person.id):
				user = person'''
		user = await self.bot.get_user(user)
		await ctx.guild.unban(user, reason = reason)
		await ctx.send(f"Unbanned **{str(user)}**")
	@commands.command()
	async def ar(self,ctx,action,msg=None,*,args=None):
		with open("data/ar.json","r") as f:
			ars = json.load(f)
		if str(ctx.guild.id) not in ars:
			ars[str(ctx.guild.id)] = {}
			ars[str(ctx.guild.id)]["amount"] = 0
			with open("data/ar.json","w") as z:
				json.dump(ars,z)
		if action == "+" or action == "add":
			if ars[str(ctx.guild.id)]["amount"] == 5:
				listcheck = checklist(ctx.author.name, ctx.author.id)
				if listcheck == 1:
					await ctx.send("You need Cerebrus Premnium for more than 5 ars.")
					return
			ars[str(ctx.guild.id)]["amount"] += 1
			ars[str(ctx.guild.id)][str(msg)] = str(args)
			with open("data/ar.json","w") as z:
				json.dump(ars,z)
			await ctx.send("added ar")
		if action == "-" or action == "remove":
			try:
				test = ars[str(ctx.guild.id)][msg]
			except KeyError:
				await ctx.send("Ar not found")
				return
			else:
				del ars[str(ctx.guild.id)][msg]
				with open("data/ar.json","w") as z:
					json.dump(ars,z)	
				await ctx.send("Removed ar")	
		if action == "list":
			em = discord.Embed(title = "Shop",color = discord.Color.green())

			for item in ars:
				name = item[str(ctx.guild.id)]

				em.add_field(name = name, value = f"trigger", inline = False)

			await ctx.send(embed = em)
	@commands.command()
	async def tag(self,ctx,action,msg=None,*,args=None):
		with open("data/ar.json","r") as f:
			ars = json.load(f)
		if str(ctx.guild.id) not in ars:
			ars[str(ctx.guild.id)] = {}
			ars[str(ctx.guild.id)]["amount"] = 0
			with open("data/tags.json","w") as z:
				json.dump(ars,z)
		if action == "+" or action == "add":
			if ars[str(ctx.guild.id)]["amount"] == 5:
				listcheck = checklist(ctx.author.name, ctx.author.id)
				if listcheck == 1:
					await ctx.send("You need Cerebrus Premnium for more than 5 ars.")
					return
			ars[str(ctx.guild.id)]["amount"] += 1
			ars[str(ctx.guild.id)][str(msg)] = str(args)
			with open("data/tags.json","w") as z:
				json.dump(ars,z)
			await ctx.send("added tag")
		if action == "-" or action == "remove":
			try:
				test = ars[str(ctx.guild.id)][msg]
			except KeyError:
				await ctx.send("Tag not found")
				return
			else:
				del ars[str(ctx.guild.id)][msg]
				with open("data/tags.json","w") as z:
					json.dump(ars,z)	
				await ctx.send("Removed tag")	
		if action == "list":
			em = discord.Embed(title = "Shop",color = discord.Color.green())

			for item in ars:
				name = item[str(ctx.guild.id)]

				em.add_field(name = name, value = f"trigger", inline = False)

			await ctx.send(embed = em)
	@commands.Cog.listener()
	async def on_message(self, message):
		with open("data/ar.json","r") as f:
			ars = json.load(f)
		if not message.author.bot:
			try:
				if message.content in ars[str(message.guild.id)]:
					msg = ars[str(message.guild.id)][str(message.content)]
					await message.channel.send(msg)
			except KeyError:
				if str(message.guild.id) not in ars:
					ars[str(message.guild.id)] = {}
					ars[str(message.guild.id)]["amount"] = 0


def setup(bot):
    bot.add_cog(moderator(bot))