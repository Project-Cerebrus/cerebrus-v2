import discord, asyncio, datetime
import traceback
def convert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s": 1,"m": 60,"h": 3600,"d": 24*3600 }
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        timeVal = int(time[:-1])
    except:
        return -2

    return timeVal*time_dict[unit]

async def paginate(bot, ctx, pages):
	main = await ctx.send(embed=pages[0])
	await main.add_reaction('⏮')
	await main.add_reaction('⏪')
	await main.add_reaction('⏹')
	await main.add_reaction('⏩')
	await main.add_reaction('⏭')
	current_page = 0
	await asyncio.sleep(1)
	'''curtime = datetime.datetime.utcnow()
	print(curtime)'''
	for i in range(50):
		'''if datetime.datetime.now - curtime >= 2:
			await main.clear_reactions()'''
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