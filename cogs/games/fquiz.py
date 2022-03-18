from utils import cmdlogger, winbtn, losebtn, checkans, toembedt
import discord
import random
import json
import aiohttp
from datetime import datetime
import asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_components import Button, ButtonStyle
global amounts
try:
	print("Successfully loaded quizlb.json")
	with open('data/quizlb.json') as f:
		amounts = json.load(f)
except FileNotFoundError:
	print("Could not load quizlb.json")


class FlagQuiz(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@commands.command(aliases=["lb"])
	async def leaderboard(self,ctx):
		with open('data/quizlb.json', 'r') as f:
			data = json.load(f)
		top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
		names = ''
		for postion, user in enumerate(top_users):
			names += f'{postion+1} - <@!{user}> | {top_users[user]}\n'
		embed = discord.Embed(title="Leaderboard")
		embed.add_field(name="Names", value=names, inline=False)
		await ctx.send(embed=embed)
	@commands.command(aliases=["fq","flagquiz"])
	async def fquiz(self,ctx):
		async with aiohttp.ClientSession() as session: 
			async with session.get("https://underscore.wtf/countries/countries.json", ssl=False) as r: data = await r.json()
		quizans=data[random.randint(0,len(data))]
		if not quizans: quizans=data[random.randint(0,len(data))]
		ansloc = random.randint(1,4) 
		ca = await checkans(data, ansloc,quizans,"name")
		btnans=[[Button(label=ca[0], emoji="🇦", style=ButtonStyle.blue, custom_id=1),Button(label=ca[1],emoji='🇧', style=ButtonStyle.blue, custom_id=2),Button(label=ca[2], emoji="🇨", style=ButtonStyle.blue, custom_id=3),Button(label=ca[3], emoji='🇩', style=ButtonStyle.blue, custom_id=4)]]
		msem = discord.Embed(title=f'Which country does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"]).set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
		message = await ctx.send(content=ctx.author.mention,embed=msem,components=btnans)
		try: 
			ansch = await self.bot.wait_for('button_click',check=lambda inter: inter.message.id == message.id and inter.user.id == ctx.author.id,timeout=15)
		except asyncio.TimeoutError: 
			return await message.edit(embed=await toembedt(f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`',quizans["flags"]),components=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]])

		if int(ansch.custom_id) == ansloc:
			with open('data/quizlb.json', 'r+') as f:
				data = json.load(f)
				if str(ctx.author.id) not in amounts.keys():
					amounts[str(ctx.author.id)] = 1
					_save()
				else:
					amounts[str(ctx.author.id)] += 1
					_save()
			await message.edit(embed=discord.Embed(title='Win',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_footer(text=f'{ctx.author} | {amounts[str(ctx.author.id)]} Point(s)',icon_url=ctx.author.avatar_url),components=await winbtn(ansloc))
		else:
			qta = await losebtn(int(ansch.custom_id),ansloc)
			await message.edit(embed=discord.Embed(title='Lose',description=f'Which country does this flag belong to?: \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["name"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]).set_footer(text=ctx.author,icon_url=ctx.author.avatar_url),components=qta[0])
def _save():
    with open('data/quizlb.json', 'w+') as f:
        json.dump(amounts, f)
def setup(bot: commands.Bot):
	cmdlogger.info("Loading FlagQuiz")
	bot.add_cog(FlagQuiz(bot))
