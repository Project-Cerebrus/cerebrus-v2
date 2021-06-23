import discord, random
from discord.ext import commands
import os
import subprocess
import asyncio
from io import StringIO
import sys
import readline
import json
import os.path
pkg = []
devs = ['775198018441838642', '746904488396324864', '750755612505407530']
async def dump(users):
	with open("data/modulus/modulus.json","w") as f:
		json.dump(users,f)
async def checkpkg(id,pkg):
	await openpkg(id)
	users = await getpkg()
	if users[str(id)][pkg] == "enabled":
		return "enabled"
	if users[str(id)][pkg] == "disabled":
		return "disabled"
async def getpkg():
	with open("data/modulus/modulus.json","r") as f:
		users = json.load(f)
	return users
async def openpkg(id):
	users = await getpkg()
	if str(id) in users:
		return
	users[str(id)] = {}
	users[str(id)]["fun"] = "enabled"
	users[str(id)]["games"] = "enabled"
	users[str(id)]["mod"] = "enabled"
	users[str(id)]["config"] = "enabled"
	users[str(id)]["misc"] = "enabled"
	users[str(id)]["utility"] = "enabled"
	users[str(id)]["snipe"] = "enabled"
	users[str(id)]["gaw"] = "enabled"
	users[str(id)]["marry"] = "enabled"
	users[str(id)]["encryption"] = "enabled"
	users[str(id)]["ticket"] = "enabled"
	users[str(id)]["vouches"] = "enabled"
	users[str(id)]["economy"] = "enabled"
	users[str(id)]["heist"] = "enabled"
	users[str(id)]["rob"] = "enabled"
	users[str(id)]["echo"] = "enabled"
	users[str(id)]["inap"] = "enabled"
	with open("data/modulus/modulus.json","w") as f:
		json.dump(users,f)	
class modulus(commands.Cog, name='Modulus'):
	def __init__(self, bot):
		self.bot = bot
	async def loadring(self,ctx):
		loadring = await ctx.send("#######........... 30% - Configuring")
		await asyncio.sleep(3)
		await loadring.edit(content="###########....... 70% - Installing")
		await asyncio.sleep(2)
		await loadring.edit(content="#################. 90% - Installing dependencies")
		await asyncio.sleep(1)
		await loadring.edit(content="################## 100% - Installed")
	async def loadring2(self,ctx):
		loadring = await ctx.send("#######........... 30% - Configuring")
		await asyncio.sleep(3)
		await loadring.edit(content="###########....... 70% - Removing")
		await asyncio.sleep(2)
		await loadring.edit(content="#################. 90% - Removing dependencies")
		await asyncio.sleep(1)
		await loadring.edit(content="################## 100% - Removed")
	@commands.command(aliases=["modulus"])
	async def mpkg(self,ctx,action=None,*,package=None):
		await openpkg(ctx.guild.id)
		ids = str(ctx.guild.id)
		if ctx.author.guild_permissions.administrator != True:
			await ctx.send("Admin permissions is required")
			return
		if action == None:
			await ctx.send("Type <p>mpkg help for all actions")
		if action == "installed":
			users = await getpkg()
			gaw = users[ids]["gaw"]
			misc = users[ids]["misc"]
			games = users[ids]["games"]
			mod = users[ids]["mod"]
			economy = users[ids]["economy"]
			fun = users[ids]["fun"]
			config = users[ids]["config"]
			ticket = users[ids]["ticket"]
			vouches = users[ids]["vouches"]
			encryption = users[ids]["encryption"]
			utility = users[ids]["utility"]
			snipe = users[ids]["snipe"]
			marry = users[ids]["marry"]
			heist = users[ids]["heist"]
			echo = users[ids]["echo"]
			rob = users[ids]["rob"]
			inap = users[ids]["inap"]
			embed = discord.Embed(title="Installed Packages",description=f"Giveaways - {gaw}\nMisc - {misc}\nGames - {games}\nMod - {mod}\nEconomy - {economy}\nFun - {fun}\nConfig - {config}\nTicket - {ticket}\nVouches - {vouches}\nEncryption - {encryption}\nUtility - {utility}\nSnipe - {snipe}\nMarry - {marry}\nRob - {rob}\nHeist - {heist}\necho - {echo}",color=discord.Color.green())
			await ctx.send(embed=embed)
		if action == "list":
			embed= discord.Embed(title = "Packages",description="Core packages:\n```\nModulus\nSettings\n```\nMain packages:\n```\nGiveaways\nMod\nEconomy\nFun\nConfig\nMisc\nSnipe\nMarry\nUtility\nGames\nEncryption\nTicket\nVouches\nRob\nHeist\n```",color=discord.Color.green())
			await ctx.send(embed=embed)
		if action == "help":
			embed = discord.Embed(title="Mpkg Help",description="*Mpkg is a package manger for @Cerebrus*\nHelp - this command\nInstall - Install a package\nReinstall - Reinstall a package\nRemove - Remove a package\nInstalled - Show installed packages\nList - List all packages",color=discord.Color.green())
			await ctx.send(embed=embed)
		if action == "install" or action == "reinstall" or action == "i" or action == "+":
			users = await getpkg()
			if users[ids][package] == "enabled":
				await ctx.send(f"{package} already installed")
				return
			if package == None:
				await ctx.send("please specify a package to install")
				return
			if package == "rob":
				users[ids]["rob"] = "enabled"
				await self.loadring(ctx)
				return
			if package == "heist":
				users[ids]["heist"] = "enabled"
				await self.loadring(ctx)
				return
			if package == "Giveaways" or package == "giveaways" or package == "gaw":
				users = await getpkg()
				users[ids]["gaw"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "economy" or package == "eco" or package == "money":
				users = await getpkg()
				users[ids]["economy"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return	
			if package == "fun":
				users = await getpkg()
				users[ids]["fun"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "games":
				users = await getpkg()
				users[ids]["games"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "cfg" or package == "config":
				users = await getpkg()
				users[ids]["config"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "misc":
				users = await getpkg()
				users[ids]["misc"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "mod":
				users = await getpkg()
				users[ids]["mod"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "snipe":
				users = await getpkg()
				users[ids]["snipe"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "marry":
				users = await getpkg()
				users[ids]["marry"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "utlility":
				users = await getpkg()
				users[ids]["utility"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "enc" or package == "encryption":
				users = await getpkg()
				users[ids]["encryption"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "ticket":
				users = await getpkg()
				users[ids]["ticket"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "vouches":
				users = await getpkg()
				users[ids]["vouches"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "echo":
				users = await getpkg()
				users[ids]["echo"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "inap":
				users = await getpkg()
				users[ids]["inap"] = "enabled"
				await dump(users)
				await self.loadring(ctx)
				return
		if action == "uninstall" or action == "remove" or action == "r" or action == "-":
			users = await getpkg()
			if users[ids][package] == "disabled":
				await ctx.send(f"{package} already removed")
				return
			if package == None:
				await ctx.send("please specify a package to remove")
				return
			if package == "Giveaways" or package == "giveaways" or package == "gaw":
				users = await getpkg()
				users[ids]["gaw"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "economy" or package == "eco" or package == "money":
				users = await getpkg()
				users[ids]["economy"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return	
			if package == "fun":
				users = await getpkg()
				users[ids]["fun"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "games":
				users = await getpkg()
				users[ids]["games"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "cfg" or package == "config":
				users = await getpkg()
				users[ids]["config"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "misc":
				users = await getpkg()
				users[ids]["misc"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "mod":
				users = await getpkg()
				users[ids]["mod"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "snipe":
				users = await getpkg()
				users[ids]["snipe"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "marry":
				users = await getpkg()
				users[ids]["marry"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "utlility":
				users = await getpkg()
				users[ids]["utility"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "enc" or package == "encryption":
				users = await getpkg()
				users[ids]["encryption"] = "disabled"
				await dump(users)
				await self.loadring(ctx)
				return
			if package == "ticket":
				users = await getpkg()
				users[ids]["ticket"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "rob":
				users[ids]["rob"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "heist":
				users[ids]["heist"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "vouches":
				users = await getpkg()
				users[ids]["vouches"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "echo":
				users = await getpkg()
				users[ids]["echo"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
			if package == "inap":
				users = await getpkg()
				users[ids]["inap"] = "disabled"
				await dump(users)
				await self.loadring2(ctx)
				return
def setup(bot):
	bot.add_cog(modulus(bot))