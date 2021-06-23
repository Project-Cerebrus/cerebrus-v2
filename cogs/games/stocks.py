import requests
import discord, random
from discord.ext import commands
import json
import os
import subprocess
import asyncio
from io import StringIO
import sys

with open("data/devs.json","r") as file:
	file = json.load(file)
	devs = file["devs"]

class stocks(commands.Cog, name='Stocks'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def stock(self,ctx,*,query):
		url = f"https://realstonks.p.rapidapi.com/{query}"

		headers = {
				'x-rapidapi-key': "a5b0325a1dmsh8e6bcbe244a2c36p1716e9jsn50d33c6c7737",
				'x-rapidapi-host': "realstonks.p.rapidapi.com"
				}

		response = requests.request("GET", url, headers=headers)

		print(response.text)
		
def setup(bot):
    bot.add_cog(stocks(bot))