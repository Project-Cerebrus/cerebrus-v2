import discord, random
from discord.ext import commands
import os
import subprocess
import asyncio
import pickle
devs = ['775198018441838642', '750755612505407530', '746904488396324864']
try:
	duckusers = pickle.load(open("static/duckusers/duckbuck.dat","rb"))
except FileNotFoundError:
	print("run _instance <action> <instance> to start instance module")
duckbuck = []
def addduckuser(id):
	duckbuck.append(id)
	duckusers.append(id)
	os.system("rm -rf static/duckbuck.dat")
	pickle.dump(duckbuck,open("static/duckusers/duckbuck.dat", "wb"))
	pickle.dump(duckusers,open("static/duckusers/duckbuck.dat", "wb"))
	return 


class instances(commands.Cog, name='Instances'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["instance"])
	async def instances(self,ctx,action=None,instance=None):
		if action == "add":
			if instance != None:
				if instance == "duckbucks":
					msg = await ctx.send(f"adding {ctx.author.mention} to duckbucks instance...")
					addduckuser(ctx.author.id)
					msg.edit(f"successfully added {ctx.author.mention} to {instance} instance\n type `_dhelp` to get started")

def setup(bot):
    bot.add_cog(instances(bot))
