from utils import cmdlogger, winbtn, losebtn, checkansf, toembedt
import discord
import random
import aiohttp
from datetime import datetime
import asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_components import Button, ButtonStyle
# flags
# add LB

class FlagQuiz(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	@commands.command(aliases=["fq","flagquiz"])
	async def fquiz(self,ctx):
		async with aiohttp.ClientSession() as session: 
			async with session.get("https://restcountries.com/v3.1/all/?fields=name,flags", ssl=False) as r: data = await r.json()
		quizans=data[random.randint(0,len(data))]
		if not quizans: quizans=data[random.randint(0,len(data))]
		ansloc = random.randint(1,4) 
		ca=await checkansf(data, ansloc,quizans)
		btnans=[[Button(label=ca[0], emoji="🇦", style=ButtonStyle.blue, custom_id=1),Button(label=ca[1],emoji='🇧', style=ButtonStyle.blue, custom_id=2),Button(label=ca[2], emoji="🇨", style=ButtonStyle.blue, custom_id=3),Button(label=ca[3], emoji='🇩', style=ButtonStyle.blue, custom_id=4)]]
		msem = discord.Embed(title=f'Which country does this flag belong to?',color=0x1860cc, timestamp = datetime.utcnow()).set_image(url=quizans["flags"]["png"])
		message = await ctx.send(embed=msem,components=btnans)
		try: 
			ansch = await self.bot.wait_for('button_click',check=lambda inter: inter.message.id == message.id and inter.user.id == ctx.author.id,timeout=15)
		except asyncio.TimeoutError: 
			return await message.edit(embed=await toembedt(f'Which country does this flag belong to? \nAnswer: `{quizans["name"]["common"]}`',quizans["flags"]["png"]),components=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]])
		
		if int(ansch.custom_id) == ansloc:
			await message.edit(embed=discord.Embed(title='Win',description=f'Which country does this flag belong to? \nAnswer: `{quizans["name"]["common"]}`', color=0x3cb556, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]["png"]),components=await winbtn(ansloc))
		else:
			qta = await losebtn(ctx,int(ansch.custom_id),ansloc)
			await message.edit(embed=discord.Embed(title='Lose',description=f'Which country does this flag belong to?: \nSelected Answer: `{btnans[0][qta[1]-1].label}` \nReal Answer: `{quizans["name"]["common"]}`',color=0xfa8e23, timestamp = datetime.utcnow()).set_thumbnail(url=quizans["flags"]["png"]),components=qta[0])

def setup(bot: commands.Bot):
	cmdlogger.info("Loading FlagQuiz")
	bot.add_cog(FlagQuiz(bot))
