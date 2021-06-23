import discord
from discord.ext import commands
import random
import asyncio
from cogs.misc.modulus import checkpkg

class Battleship(commands.Cog, name='Battleship'):
    """Play the old game called Battleship!"""

    def __init__(self, bot):
        self.bot = bot
        self.positions = [
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
        'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
        'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10',
        'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10'
        ]

    @commands.command(pass_context=True, aliases=["seabattle"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def battleship(self, ctx):
        pkg = "games"
        check = await checkpkg(ctx.guild.id,pkg)
        if check == "enabled":
          print("[Games]: Enabled")
        if check == "disabled":
          await ctx.send("command disabled, use mpkg to reinstall")
          return
        """Play Battleship with the bot. I swear I won't cheat ;)"""
        status = await ctx.send("Generating my sea...")
        botsea = []
        for i in range(10):
            position = random.choice(self.positions)
            while position in botsea:
                position = random.choice(self.positions)
            botsea.append(position)
        await asyncio.sleep(1) # so it looks a bit legit like it's actually doing something.
        await status.edit(content="Generating your sea...")
        usersea = []
        for i in range(10):
            position = random.choice(self.positions)
            while position in usersea:
                position = random.choice(self.positions)
            while position in botsea:
                position = random.choice(self.positions)
            usersea.append(position)
        await asyncio.sleep(1) # again, just so it looks legit like it's actually doing something.
        await ctx.send("Your ships are located at: **{}**.\nStarting battle now. You can always say 'stop' to stop or 'help' for help.".format("**, **".join(usersea)))
        await status.delete()
        board = "A1 A2 A3 A4 A5 A6 A7 A8 A9 A10\nB1 B2 B3 B4 B5 B6 B7 B8 B9 B10\nC1 C2 C3 C4 C5 C6 C7 C8 C9 C10\nD1 D2 D3 D4 D5 D6 D7 D8 D9 D10\nE1 E2 E3 E4 E5 E6 E7 E8 E9 E10\nF1 F2 F3 F4 F5 F6 F7 F8 F9 F10\nG1 G2 G3 G4 G5 G6 G7 G8 G9 G10\nH1 H2 H3 H4 H5 H6 H7 H8 H9 H10\nI1 I2 I3 I4 I5 I6 I7 I8 I9 I10\nJ1 J2 J3 J4 J5 J6 J7 J8 J9 J10"
        boardMsg = await ctx.send("```fix\n" + board + "```")
        first = random.choice([False, True])
        if first:
            status = await ctx.send("I'll go first.")
            while True:
                bomb = random.choice(self.positions)
                if bomb in usersea:
                    usersea.remove(bomb)
                    if len(usersea) > 0:
                        await status.edit(content="I've hit one of your ships! I hit {}, you have **{}** left ({} ships). Your turn.".format(bomb, "**, **".join(usersea), len(usersea)))
                        await asyncio.sleep(1.5)
                    else:
                        await status.edit(content="I've hit your last ship! I hit {}, so I win. I had **{}** left ({} ships)".format(bomb, "**, **".join(botsea), len(botsea)))
                        break
                else:
                    await asyncio.sleep(1.5)
                    await status.edit(content="I missed, your turn.")
                bomb = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
                if (bomb == None) or (bomb.content.upper() == "STOP"):
                    await status.edit(content="K then, I'll stop. I had **{}** left ({} ships).".format("**, **".join(botsea), len(botsea)))
                    try:
                        await bomb.delete()
                    except:
                        pass
                    break
                elif (bomb.content.upper() not in self.positions) or (bomb.content.upper() == "HELP"):
                    await ctx.send("In this game you have to bomb the bot's ship, "
                    "you can do this by saying {0} for example, this will bomb {0}."
                    " If there's a ship there that ship will be destroyed, if there's no ship there the bomb will explode in the water."
                    " So when it's your turn you'll just have to say A1, B5, G9, it goes all the way up to J10."
                    " And just so I have to code less, it's now the bot's turn.".format(random.choice(self.positions)))
                elif bomb.content.upper() not in board:
                    await status.edit(content="You already picked that one, my turn now.")
                    await asyncio.sleep(1.5)
                elif bomb.content.upper() in botsea:
                    botsea.remove(bomb.content.upper())
                    if len(botsea) > 0:
                        await status.edit(content="You've hit one of my ships! I have {} ships left.".format(len(botsea)))
                        if not bomb.content.upper().endswith("10"):
                            board = board.replace(bomb.content.upper() + " ", "XX ")
                        else:
                            board = board.replace(bomb.content.upper(), "XX")
                        await boardMsg.edit(content="```fix\n" + board + "```")
                        await asyncio.sleep(1.5)
                    else:
                        await status.edit(content="You've hit my last ship! You win!")
                        break
                else:
                    await status.edit(content="You missed, my turn.")
                    if not bomb.content.upper().endswith("10"):
                        board = board.replace(bomb.content.upper() + " ", "XX ")
                    else:
                        board = board.replace(bomb.content.upper(), "XX")
                    await boardMsg.edit(content="```fix\n" + board + "```")
                    try:
                        await bomb.delete()
                    except:
                        pass
                    await asyncio.sleep(1.5)
        else:
            status = await ctx.send("You'll go first.")
            while True:
                bomb = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author, timeout = 30)
                if (bomb == None) or (bomb.content.upper() == "STOP"):
                    await status.edit(content="K then, I'll stop. I had **{}** left ({} ships).".format("**, **".join(botsea), len(botsea)))
                    try:
                        await bomb.delete()
                    except:
                        pass
                    break
                elif (bomb.content.upper() not in self.positions) or (bomb.content.upper() == "HELP"):
                    example = random.choice(self.positions)
                    await ctx.send("In this game you have to bomb the bot's ship, "
                    "you can do this by saying {0} for example, this will bomb {0}."
                    " If there's a ship there that ship will be destroyed, if there's no ship there the bomb will explode in the water."
                    " So when it's your turn you'll just have to say A1, B5, G9, it goes all the way up to J10."
                    " And just so I have to code less, it's now the bot's turn.".format(example))
                elif bomb.content.upper() not in board:
                    await status.edit(content="You already picked that one, my turn now.")
                    await asyncio.sleep(1.5)
                elif bomb.content.upper() in botsea:
                    botsea.remove(bomb.content.upper())
                    if len(botsea) > 0:
                        await status.edit(content="You've hit one of my ships! I have {} ships left.".format(len(botsea)))
                        board = board.replace(bomb.content.upper(), "XX")
                        if not bomb.content.upper().endswith("10"):
                            board = board.replace(bomb.content.upper() + " ", "XX ")
                        else:
                            board = board.replace(bomb.content.upper(), "XX")
                        await asyncio.sleep(1.5)
                    else:
                        await status.edit(content="You've hit my last ship! You win!")
                        break
                else:
                    await status.edit(content="You missed, my turn.")
                    if not bomb.content.upper().endswith("10"):
                        board = board.replace(bomb.content.upper() + " ", "XX ")
                    else:
                        board = board.replace(bomb.content.upper(), "XX")
                    await boardMsg.edit(content="```fix\n" + board + "```")
                    try:
                        await bomb.delete()
                    except:
                        pass
                    await asyncio.sleep(1.5)
                bomb = random.choice(self.positions)
                if bomb in usersea:
                    usersea.remove(bomb)
                    if len(usersea) > 0:
                        await status.edit(content="I've hit one of your ships! I hit {}, you have **{}** left ({} ships). Your turn.".format(bomb, "**, **".join(usersea), len(usersea)))
                        await asyncio.sleep(1.5)
                    else:
                        await status.edit(content="I've hit your last ship! I hit {}, so I win. I had **{}** left ({} ships)".format(bomb, "**, **".join(botsea), len(botsea)))
                        break
                else:
                    await asyncio.sleep(1.5)
                    await status.edit(content="I missed, your turn.")
            
def setup(bot):
    bot.add_cog(Battleship(bot))  