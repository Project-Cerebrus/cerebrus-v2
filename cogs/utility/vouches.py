import asyncio
import math
from datetime import datetime
import discord, random
import os
import subprocess
from discord.ext import commands
import json

prefix = '_'
footer_text = f'type {prefix}help to see my commands'
embed_color = 0x3cd3f6
error_embed_color = 0xff0000


def write(self):
    with open('data/vouch.json', 'w') as file:
        file.write(json.dumps(data, indent=4, sort_keys=True))


async def embed(ctx, title: str, description: str):
    _embed = discord.Embed(title=title, description=description, color=embed_color)
    _embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    _embed.set_footer(text=footer_text)
    return await ctx.send(embed=_embed)


async def error_embed(ctx, title: str, description: str):
    _embed = discord.Embed(title=":x: " + title, description=description, color=error_embed_color)
    _embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    _embed.set_footer(text=footer_text)
    return await ctx.send(embed=_embed)


def server_init(self, ctx):
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
        write(self)
        return False

    return True


def author_init(self, ctx):
    if not server_init(self, ctx):
        return False

    if ctx.author.id != self.bot.user.id and not str(ctx.author.id) in data[str(ctx.guild.id)]:
        #print(f'User {ctx.author} in {ctx.guild.name} has no vouch data, creating fresh vouch data for them.')
        data[str(ctx.guild.id)][str(ctx.author.id)] = {"Username": str(ctx.author), "Vouches": {}}
        write(self)
        return False

    return True




if os.path.isfile('data/vouch.json'):
  with open('data/vouch.json', 'r') as file:
    data = json.loads(file.read())
    if not data:
      data = {}
else:
	data = {}

class Vouches(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vouch(self, ctx, member: discord.Member = None, *, message: str = None):
        server_init(self, ctx)
        author_init(self, ctx)

        if not member:
            await error_embed(ctx, 'Please mention a member to vouch.', None)
            return

        if member.id == ctx.author.id:
            await error_embed(ctx, 'You cannot vouch yourself.', None)
            return

        if member.id == self.bot.user.id:
            await error_embed(ctx, 'I am not vouchable!', None)
            return

        if not message:
            await error_embed(ctx, f'Please add a message to your vouch. Usage: `{prefix}vouch @user Message here`', None)
            return

        if not str(member.id) in data[str(ctx.guild.id)]:
            # print(f'User {member} in {ctx.guild.name} has no vouch data, creating fresh vouch data for them.')
            data[str(ctx.guild.id)][str(member.id)] = {"Username": str(member), "Vouches": {}}
            write(self)

        if str(ctx.author.id) in data[str(ctx.guild.id)][str(member.id)]["Vouches"]:
            await error_embed(ctx, 'You have already vouched this user.', None)
            return

        if len(message) > 250:
            await error_embed(ctx, 'Please limit your vouch message to 250 characters.', None)
            return

        if len(message.splitlines()) > 3:
            await error_embed(ctx, 'Please limit your vouch message to 3 newlines.', None)
            return

        data[str(ctx.guild.id)][str(member.id)]["Vouches"][str(ctx.author.id)] = {"Message": message, "Username": str(ctx.author), "Date": datetime.now().strftime('%Y-%m-%d')}
        write(self)

        await embed(ctx, f'✅ Vouched __{member}__', f'**With message:**\n```{message}```' if message is not None else None)

    @vouch.error
    async def vouch_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await error_embed(ctx, 'Invalid member or invalid message string.', '*(try re-typing the username?)*')

    
    @commands.command()
    async def vouches(self, ctx, member: discord.Member = None):
        server_init(self, ctx)
        author_init(self, ctx)

        if not member:
            member = ctx.author

        if member.id == self.bot.user.id:
            await error_embed(ctx, "I don't have any vouches!", None)
            return

        vouches = data[str(ctx.guild.id)][str(member.id)]["Vouches"]
        if len(vouches) < 1:
            await error_embed(ctx, "It looks like you don't have any vouches :(" if member.id == ctx.author.id else "This user does not have any vouches.", None)
            return

        pages = []
        pages_count = math.ceil(len(vouches) / 5)
        for i in range(1, pages_count + 1):
            page_contents = ''
            for user in {k: vouches[k] for k in list(vouches)[(5 * i) - 5 if i > 1 else 0:5 * i]}:
                page_contents += f"<@{user}> - *{vouches[user]['Date']}*\n```{vouches[user]['Message']}```\n"
            pages.append(page_contents)

        cur_page = 1

        embed = discord.Embed(title=f"All vouches for {member}", description=f"__Total Vouches:__ **{len(vouches)}**\n\n{pages[cur_page-1]}", color=embed_color).set_footer(
            text=f'Page {cur_page}/{pages_count}').set_thumbnail(url=member.avatar_url).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=embed)

        back = "⬅️"
        forward = "➡️"

        await message.add_reaction(back)
        await message.add_reaction(forward)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [back, forward] and reaction.message.id == message.id
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)
                # waiting for a reaction to be added - times out after 30 seconds

                if str(reaction.emoji) == forward and cur_page != pages_count:
                    cur_page += 1
                    await message.edit(embed=discord.Embed(title=f"All vouches for {member}", description=f"__Total Vouches:__ **{len(vouches)}**\n\n{pages[cur_page-1]}", color=embed_color).set_footer(
                        text=f'Page {cur_page}/{pages_count}').set_thumbnail(url=member.avatar_url).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url))
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == back and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=discord.Embed(title=f"All vouches for {member}", description=f"__Total Vouches:__ **{len(vouches)}**\n\n{pages[cur_page-1]}", color=embed_color).set_footer(
                        text=f'Page {cur_page}/{pages_count}').set_thumbnail(url=member.avatar_url).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url))
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    @vouches.error
    async def vouches_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await error_embed(ctx, 'Invalid member', '*(try re-typing the username?)*')

    @commands.command()
    async def vleaderboard(self, ctx):
        server_init(self, ctx)
        author_init(self, ctx)

        all_members = {}
        for user in data[str(ctx.guild.id)]:
            all_members[user] = len(data[str(ctx.guild.id)][user]["Vouches"])

        # Sort the users by their vouches
        top10 = {k: v for k, v in sorted(all_members.items(), key=lambda item: item[1])}

        s = ''
        for i in range(1, 11):
            try:
                if [*top10.values()][-i] < 1:
                    continue

                s += f"{i}) <@{[*top10.keys()][-i]}> - **{[*top10.values()][-i]}** Vouches\n"
            except IndexError:
                pass

        if s == '':
            await error_embed(ctx, "Looks like nobody in this server has any vouches.", None)
            return

        await embed(ctx, 'Vouch Leaderboard', s)


def setup(bot):
    bot.add_cog(Vouches(bot))
	