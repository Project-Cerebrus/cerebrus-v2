import discord
import asyncio
import math
import random
from discord.ext import commands
from cogs.misc.modulus import checkpkg

class Player:
    def __init__(self, member):
        self.member = member
        self.hp = 100
        self.defense = 0


class Fight(commands.Cog, name='Vs'):
    def __init__(self, bot):
        self.bot = bot

    async def attack(self, player):
        damage = int(
            (math.pow(random.randrange(30, 50), 1.35) / 10) * 1 - player.defense / 100
        )
        player.hp -= damage
        return damage

    async def kick(self, player):
      damage = int(
					(math.pow(random.randrange(50, 95), 1.35) / 10) * 1 - player.defense / 100
			)
      player.hp -= damage
      return damage

    async def fall(self, player):
      damage = int(
					(math.pow(random.randrange(1, 50), 1.35) / 10) * 1 - player.defense / 100
			)
      player.hp -= damage
      return damage

    async def defend(self, player):
        player.defense += 3
        heal = random.randrange(1, 20)
        player.hp += heal
        if player.hp > 115:
            player.hp = 115
            heal = 0
        if player.defense > 45:
            player.defense = 45
            return heal, True
        return heal, False

    async def turn(self, ctx, p1, p2):
        await ctx.send(
            f"{p1.member.mention} **Choose a move**:  `attack`, `kick`, `defend`, `escape`"
        )
        try:
            choice = await self.bot.wait_for(
                "message",
                check=lambda m: m.channel == ctx.channel
                and m.author == p1.member
                and (
                    m.content == "attack"
                    or m.content == "defend"
                    or m.content == "escape"
										or m.content == "kick"
                ),
                timeout=30,
            )
            if choice.content.startswith("defend"):
                healAmount, defenseMaxed = await self.defend(p1)
                if defenseMaxed:
                    await ctx.send(
                        f"You healed for `{healAmount}`, but your defense is maxed out"
                    )
                else:
                    await ctx.send(
                        f"You healed for `{healAmount}`, and your defense rose by `3`"
                    )
            elif choice.content.startswith("attack"):
                damage = await self.attack(p2)
                await ctx.send(f"You attacked dealing **{damage}** damage")
            elif choice.content.startswith("kick"):
                fall = random.randrange(1,4)
                if fall == 0:
                  damage = await self.kick(p2)
                  await ctx.send(f"You kicked dealing **{damage}** damage")
                if fall == 1:
                  damage = await self.kick(p2)
                  await ctx.send(f"You kicked dealing **{damage}** damage")
                if fall == 2:
                  damage = await self.kick(p2)
                  await ctx.send(f"You kicked dealing **{damage}** damage")
                if fall == 3:
                  damage = await self.kick(p1)
                  await ctx.send(f"You fell taking **{damage}** damage")
            elif choice.content.startswith("escape"):
                await ctx.send(f"{p1.member.name} tried escaping. **tried**")
                await ctx.send(
                    embed=discord.Embed(
                        title="CRITICAL HIT",
                        description="9999 Damage!",
                        colour=discord.Color.red(),
												
                    )
                )
                p1.hp = -9999

        except asyncio.TimeoutError:
            await ctx.send(
                f"`{p2.member.name}` got tired of waiting and bonked `{p1.member.name}` on the head."
            )
            await ctx.send(
                embed=discord.Embed(
                    title="CRITICAL HIT",
                    description="9999 Damage!",
                    colour=discord.Color.red(),
                )
            )
            p1.hp = -9999
        await ctx.send(
            f" \n {p1.member.mention} STATS:  **HP:** `{p1.hp}` |  **Defense**: `{p1.defense}`\n \n {p2.member.mention} STATS: **HP**: `{p2.hp}` |  **Defense**: `{p2.defense}` \n"
        )

    @commands.command(name="fight", aliases=["battle"], brief="Fight a friend, or foe!")
    async def fight_command(self, ctx, opponent: discord.Member=None):
        pkg = "games"
        check = await checkpkg(ctx.guild.id,pkg)
        if check == "enabled":
          print("[Games]: Enabled")
        if check == "disabled":
          await ctx.send("command disabled, use mpkg to reinstall")
          return
        """Fight another member in the Discord server with the fight command, you can attack, defend, or flee!"""
        #if ctx.channel.id in self.occupied:
            #await ctx.send("This battlefield is occupied")

            #self.occupied.append(ctx.channel.id)
        if opponent == None:
          await ctx.send("please mention a member to fight")
        if opponent == ctx.message.author:
            await ctx.send(f"{ctx.author.mention} hurt itself in its confusion.")
            #self.occupied.remove(ctx.channel.id)
            return
        if opponent.bot:
            await ctx.send(
                f"You try fighting the robot.\n\n*pieces of you can be found cut up on the battlefield*"
            )
            #self.occupied.remove(ctx.channel.id)
            return
        if (random.randrange(0, 2)) == 0:
            p1 = Player(ctx.message.author)
            p2 = Player(opponent)
        else:
            p1 = Player(opponent)
            p2 = Player(ctx.message.author)
        await ctx.send(
            embed=discord.Embed(
                title="Battle",
                description=f"""{ctx.author.mention} is challenging {opponent.mention}!
        let the games begin.""",
            )
        )
        await ctx.send(f"{p1.member.mention} starts,{p2.member.mention}!")
        toggle = True
        while p1.hp >= 0 and p2.hp >= 0:
            if toggle:
                await self.turn(ctx, p1, p2)
                toggle = False
            else:
                await self.turn(ctx, p2, p1)
                toggle = True

        #self.occupied.remove(ctx.channel.id)
        if p1.hp > 0:
            winner = p1
            loser = p2
        else:
            winner = p2
            loser = p1
        case = random.randrange(0, 6)
        if case == 0:
            await ctx.send(
                f"{winner.member.mention} is having human meat for dinner tonight."
            )
        if case == 1:
            await ctx.send(
                f"{winner.member.mention} is dancing on `{loser.member.name}`'s corpse."
            )
        if case == 2:
            await ctx.send(f"{winner.member.mention} did some good stabbing.")
        if case == 3:
            await ctx.send(f"{winner.member.mention} Is victorious!")
        if case == 4:
          await ctx.send(f"{winner.member.mention} unleashed their inner killer beware...")
        if case == 5:
          await ctx.send(f"{winner.member.mention} Kaneki lended his horrible terrifying power!")


	

  
def setup(bot):
    bot.add_cog(Fight(bot))