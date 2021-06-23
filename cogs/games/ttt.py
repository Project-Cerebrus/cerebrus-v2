import discord, random
from discord.ext import commands
import os
import subprocess
import asyncio
import random
from cogs.misc.modulus import checkpkg
devs = ['775198018441838642', '750755612505407530', '746904488396324864']
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
class ttt(commands.Cog, name='ttt'):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(aliases=["ttt"])
	async def tictactoe(self,ctx,p1: discord.Member, p2: discord.Member):
			pkg = "games"
			check = await checkpkg(ctx.guild.id,pkg)
			if check == "enabled":
				print("[Games]: Enabled")
			if check == "disabled":
				await ctx.send("command disabled, use mpkg to reinstall")
				return
			p1 = ctx.author
			global count
			global player1
			global player2
			global turn
			global gameOver

			if gameOver:
					global board
					board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
									":white_large_square:", ":white_large_square:", ":white_large_square:",
									":white_large_square:", ":white_large_square:", ":white_large_square:"]
					turn = ""
					gameOver = False
					count = 0

					player1 = p1
					player2 = p2

					# print the board
					line = ""
					for x in range(len(board)):
							if x == 2 or x == 5 or x == 8:
									line += " " + board[x]
									await ctx.send(line)
									line = ""
							else:
									line += " " + board[x]

					# determine who goes first
					num = random.randint(1, 2)
					if num == 1:
							turn = player1
							await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
							await ctx.send("type `<prefix>place x` eg. `_place 1`")
					elif num == 2:
							turn = player2
							await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
							await ctx.send("type `<prefix>place x` eg. `_place 1`")
			else:
					await ctx.send("A game is already in progress! Finish it before starting a new one.")

	@commands.command()
	async def place(self,ctx, pos: int,*,args=None):
		if args != None:
			if args == "exit":
				await ctx.send("exited game...")
				return
		global turn
		global player1
		global player2
		global board
		global count
		global gameOver

		if not gameOver:
				mark = ""
				if turn == ctx.author:
						if turn == player1:
								mark = ":regional_indicator_x:"
						elif turn == player2:
								mark = ":o2:"
						if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
								board[pos - 1] = mark
								count += 1

								# print the board
								line = ""
								for x in range(len(board)):
										if x == 2 or x == 5 or x == 8:
												line += " " + board[x]
												await ctx.send(line)
												line = ""
										else:
												line += " " + board[x]
								await ctx.send("type `<prefix>place x` eg. `_place 1`")

								checkWinner(winningConditions, mark)
								print(count)
								if gameOver == True:
										await ctx.send(mark + " wins!")
								elif count >= 9:
										gameOver = True
										await ctx.send("It's a tie!")

								# switch turns
								if turn == player1:
										turn = player2
								elif turn == player2:
										turn = player1
						else:
								await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
				else:
						await ctx.send("It is not your turn.")
		else:
				await ctx.send("Please start a new game using the !tictactoe command.")

	@tictactoe.error
	async def tictactoe_error(ctx, error):
			print(error)
			if isinstance(error, commands.MissingRequiredArgument):
					await ctx.send("Please mention 2 players for this command.")
			elif isinstance(error, commands.BadArgument):
					await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

def checkWinner(winningConditions, mark):
		global gameOver
		for condition in winningConditions:
				if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
						gameOver = True


def setup(bot):
    bot.add_cog(ttt(bot))