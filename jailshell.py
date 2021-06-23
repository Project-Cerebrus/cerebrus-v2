import os, discord, keep_alive
from discord.ext import commands
import aiohttp
import subprocess
pfp_path = "/home/runner/unamed-kacekull/jailshell.png"

fp = open(pfp_path, 'rb')
pfp = fp.read()
prefixes = ['-', '//', '_']

bot = commands.Bot(command_prefix = prefixes,case_insensitive = True, intents = discord.Intents.all())

@bot.event
async def on_ready():
	print('Logged in')
	print("I'm online and working")
	for i in range(10000):
	    await bot.change_presence(status = discord.Status.do_not_disturb,activity=discord.Game(name='Quarantined by my Devs'))

@bot.command(aliases = ['login', 'comeback'])
async def restore(ctx):
	devs = ['775198018441838642', '750755612505407530', '746904488396324864']
	if str(ctx.author.id) not in devs:
		await ctx.reply(f'Only **The Devs** can log me in.\nCurrent Devs are <@{devs[0]}>, <@{devs[1]}>, <@{devs[2]}>')
		return
	embed=discord.Embed(title = "Logged In", description = f"With Latency {round(bot.latency*1000)}", color = discord.Color.red())
	await ctx.send(embed=embed)
	os.system("python main.py")



@bot.command()
async def about(ctx):
	await ctx.send("Jailshell is a suspension of the bot with only 2 commands, login to get back into play and about this command and sh to run repl.it shell from bot. Jailshell is used to suspend the bot in times of emergency")


@bot.command()
async def sh(ctx,*,args):
	os.system(args)
	outputsh = subprocess.check_output(args, shell=True)
	await ctx.send("Jailshell executed (`" + args + "`)" )
	await ctx.send(outputsh)



keep_alive.keep_alive()
bot.run('ODE4MDA3NDcwMTEwMDE1NDkw.YERy0g.gP7vkWhRZF0iNuujsjDhULnC3Vc')

