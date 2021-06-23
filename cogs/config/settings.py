import discord, json, random, asyncio
from discord.ext import commands
from discord import utils
import importlib
from discord import Webhook, RequestsWebhookAdapter, File
import requests
import TenGiphPy, os
#from googlesearch import search
import time
async def open_guild(guild):

	guilds = await get_guilds_data()

	if str(guild.id) in guilds:
		return False
	else:
		guilds[str(guild.id)] = {}
		guilds[str(guild.id)]["prefix"] = '_'
		guilds[str(guild.id)]["muterole"] = None
		guilds[str(guild.id)]["heistping"] = None

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
		guilds[str(guild.id)]["status"] = None

	with open('data/tolock.json','w') as f:
		json.dump(guilds,f)

	return True


async def get_lock_data():
	with open('data/tolock.json','r') as f:
		guilds = json.load(f)

	return guilds

async def restart():
	os.system("python restart.py")
	return
class config(commands.Cog, name='Settings'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = 'prefixset', aliases = ['prefix'])
	@commands.has_permissions(manage_guild=True)
	async def prefixset(self, ctx, *, feed):
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		guilds[str(guild.id)]["prefix"] = feed
		with open('data/config.json','w') as f:
			json.dump(guilds,f)
		await ctx.reply(f'Successfully set the prefix for this server to `{feed}`')
		await restart()
	
	@commands.command(name='setmuterole', aliases = ['setm','setmute'])
	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def setmuterole(self, ctx, *, feed):
		await open_guild(ctx.guild)
		guilds = await get_guilds_data()
		guild = ctx.guild
		if feed.startswith('<@&'):
			feed = feed.replace('<@&', '').replace('>', '')
		guilds[str(guild.id)]["muterole"] = feed 
		with open('data/config.json','w') as f:
			json.dump(guilds,f)
		muterole = guild.get_role(int(feed))
		await ctx.reply(f'Successfully set the MuteRole to `{muterole.name}`\nConfiguring Muterole in all channels...')
		await ctx.channel.trigger_typing()
		for channel in ctx.guild.channels:
				overwrite = channel.overwrites_for(muterole)
				overwrite.send_messages = False
				await channel.set_permissions(muterole, overwrite=overwrite)
		await ctx.reply('Successfully configured the MuteRole')
		
	@commands.command(name='lockdownset', aliases = ['lds'])
	@commands.has_permissions(manage_guild=True)
	async def lds(self, ctx, type=None, *, input=None):
		await open_lock(ctx.guild)
		locks = await get_lock_data()
		guild = ctx.guild
		if type == 'addchan' or type == 'addchannel':
			inputs = input.split()
			final = []
			for input in inputs:
				input = input.replace('<#','').replace('>','')
				try:
					trial = int(input)
				except:
					return await ctx.reply('Only integers or channel mentions.')
				final.append(input)
			if locks[str(guild.id)]["channels"] == []:
				locks[str(guild.id)]["channels"] = final
				with open('data/tolock.json','w') as f:
					json.dump(locks,f)
			else:
				for x in final:
					if x in locks[str(guild.id)]["channels"]:
						return await ctx.reply('One of these channels are already in the list... Try again.')
					try:
						trial = int(x)
					except:
						return await ctx.reply('Only integers or channel mentions.')
					locks[str(guild.id)]["channels"].append(str(x))
					with open('data/tolock.json','w') as f:
						json.dump(locks,f)
			await ctx.send('Successfully updated!')

		elif type == 'removechan' or type == 'removechannel':
			inputs = input.split()
			final = []
			for input in inputs:
				input = input.replace('<#','').replace('>','')
				final.append(input)
			if locks[str(guild.id)]["channels"] == []:
				return await ctx.reply('You don\'t have any channels to remove...')
			else:
				for x in final:
					if x not in locks[str(guild.id)]["channels"]:
						return await ctx.reply('One of these channels are not in the list... Try again.')
					locks[str(guild.id)]["channels"].remove(str(x))
					with open('data/tolock.json','w') as f:
						json.dump(locks,f)
			await ctx.send('Successfully updated!')

		elif type == 'channels':
			final = []
			for channel in locks[str(guild.id)]["channels"]:
				channel = ctx.guild.get_channel(int(channel))
				x = (f"`{channel.id}` - {channel.mention}")
				final.append(x)
			final = str(final).replace('\'','').replace(',','\n').replace('[','').replace(']','')
			embed = discord.Embed(title = f'{ctx.guild.name}\'s Lockdown Channels', description = f'{final}', color = discord.Color.green())
			await ctx.send(embed=embed)

		elif type == 'reset':
			locks[str(guild.id)]["channels"] = None
			with open('data/tolock.json','w') as f:
				json.dump(locks,f)
			await ctx.send('Successfully Reset LockDown Settings')
		else:
			embed = (discord.Embed(title = 'LockDown Set | lds', description = 'Set some particular channels to Lock or Unlock when `lockdown`/`unlockdown` are used\n\nUsage: `<p>lockdown dank memer is down`, `<p>unlockdown dank memer is back`', colour = discord.Color.green())
			.add_field(name = 'addchan', value = 'Add a channel to the current list', inline = False)
			.add_field(name = 'removechan', value = 'Remove a channel from the current list', inline = False)
			.add_field(name = 'channels', value = 'View the current list of channels', inline = False)
			.add_field(name = 'reset', value = 'Completely reset the current lockdown settings', inline = False))
			await ctx.send(embed=embed)

	@commands.command(name = 'configure')
	@commands.has_permissions(manage_guild=True)
	async def configure(self,ctx):
		null = "null"
		embed = (discord.Embed(title = 'Configuring...', description = 'Started Config.json Package\n #......... - 10%', colour = discord.Color.green()))
		sentfig = await ctx.send(embed=embed)
		await asyncio.sleep(3)
		newem = (discord.Embed(title = 'Configuring...', description = 'Started Config.json Package', colour = discord.Color.green())
		.add_field(name = 'Default Prefix Set', value = f'`_` has been set as the prefix.\nUse `_prefixset <new_prefix>` to change it.\n ###....... - 30%', inline = False))
		await sentfig.edit(embed=newem)
		newem = newem.add_field(name = 'Trying to find a Muterole...', value = '** **', inline = False)
		await sentfig.edit(embed=newem)
		muterole = None
		for r in ctx.guild.roles:
			if 'muted' in r.name.lower():
				muterole = r
			if 'cerebrus' in r.name.lower():
				selfrole = r
			else:
				pass
		await asyncio.sleep(5)
		if muterole != None:
			newem = (discord.Embed(title = 'Configuring...', description = 'Started Config.json Package', colour = discord.Color.green())
			.add_field(name = 'Default Prefix Set', value = f'`_` has been set as the prefix.\nUse `_prefixset <new_prefix>` to change it.', inline = False)
			.add_field(name = 'Found a Muterole!', value = f'**{muterole.name}** has been set as the Muterole.\nUse `_setm <roleid/rolemention>` to change it.\n ######.... - 60%', inline = False))
			await sentfig.edit(embed=newem)
			newem = newem.add_field(name = 'Configuring Muterole...', value = '** **', inline = False)
			await sentfig.edit(embed=newem)
			for channel in ctx.guild.channels:
				overwrite = channel.overwrites_for(muterole)
				overwrite.send_messages = False
				await channel.set_permissions(muterole, overwrite=overwrite)
			try:
				await muterole.edit(position = selfrole.position-1)
			except:
				pass
			newem = (discord.Embed(title = 'Configuring...', description = 'Started Config.json Package', colour = discord.Color.green())
			.add_field(name = 'Default Prefix Set', value = f'`_` has been set as the prefix.\nUse `_prefixset <new_prefix>` to change it.', inline = False)
			.add_field(name = 'Found a Muterole!', value = f'**{muterole.name}** has been set as the Muterole.\nUse `_setm <roleid/rolemention>` to change it.', inline = False)
			.add_field(name = 'Configured Muterole', value = 'Locked the Muterole in all channels\n ######.... - 60%', inline = False))
			await asyncio.sleep(5)
			await sentfig.edit(embed=newem)
		else:
			newem = newem.add_field(name = 'Couldn\'t find a Muterole', value = 'Use `_setm <roleid/rolemention>` to set it.', inline = False)
			await sentfig.edit(embed=newem)
		'''newem = newem.add_field(name = 'Trying to Find Heist Ping role', value = '** **')
		heistping = None
		for r in ctx.guild.roles:
			if 'heist ping' in r.lower():
				heistping = r
			else:
				pass
		await asyncio.sleep(5)
		if heistping != None:
			newem = newem.add_field(name = 'Found Heist Ping!', value = f'{muterole.name} has been set as the Heist Ping role.\nUse `_setm <roleid/rolemention>` to change it.)
			await sentfig.edit(embed=newem)
		else:
			newem = (discord.Embed(title = 'Configuring...', description = 'Started Config.json Package', colour = discord.Color.green())
			.add_field(name = 'Couldn\'t find a Muterole', value = 'Use `_setm <roleid/rolemention>` to set it.'))
			await sentfig.edit(embed=newem)'''
		input4guild = {str(ctx.guild.id): {"prefix": "_", "muterole": str(muterole.id), "heistping": null, "heistmanager": null, "auctioneer": null}}
		with open('data/config.json', 'w') as json_file:
			json.dump(input4guild, json_file)
		await asyncio.sleep(10)
		newem = discord.Embed(title = 'Completed Configuration\n ########## - 100%', color = discord.Color.green())
		await sentfig.edit(embed=newem)


# mute no work imma clean up help cmd
def setup(bot):
    bot.add_cog(config(bot))