import os
import sys
import random
import asyncio
from datetime import datetime
from pywikihow import search_wikihow
from utils import cmdlogger, logger, format_seconds

import discord
from discord.ext import commands
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext, SlashContext
from discord_components import Button, ButtonStyle
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

async def httpscat(ctx,err):
	httplist =[100,101,102,200,201,202,203,204,206,207,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,420,421,422,423,424,425,426,429,431,444,450,451,497,498,499,500,501,502,503,504,506,507,508,509,510,511,521,523,525,599]
	if err == None: err = random.choice(httplist)
	if err not in httplist: err = random.choice(httplist)
	await ctx.send(f"https://http.cat/{err}.jpg")

async def timeup(ctx,stt):
	upts = str((stt).timestamp()).split('.')[0]
	embed = discord.Embed(title="Uptime", description=f"Current uptime: \n> {format_seconds(round((datetime.now() - stt).total_seconds()))}\n\nDiscord Timestamps: \n> <t:{upts}:F> (<t:{upts}:R>)",color=0x28acb8,timestamp = datetime.utcnow())
	await ctx.send(embed=embed)
	
async def brr(ctx,eng):
	await ctx.send(f'English: {eng} \nBraille: {(str(eng).lower()).replace("a", "⠁").replace("b", "⠃").replace("c", "⠉").replace("d", "⠙").replace("e", "⠑").replace("f", "⠋").replace("g", "⠛").replace("h", "⠓").replace("i", "⠊").replace("j", "⠚").replace("k", "⠅").replace("l", "⠅").replace("m", "⠍").replace("n", "⠝").replace("o", "⠕").replace("p", "⠏").replace("q", "⠟").replace("r", "⠗").replace("s", "⠎").replace("t", "⠞").replace("u", "⠥").replace("v", "⠧").replace("w", "⠺").replace("x", "⠭").replace("y", "⠽").replace("z", "⠵")}')

async def whs(wiki):
		howtos = ""
		max_results = 1
		how_tos = search_wikihow(wiki, max_results)
		howtoto =  how_tos[0]
		for step in range(len(howtoto.steps)):
			strep = howtoto.steps[step]
			howtos = howtos + str(strep.number) + " - " + strep.summary + "\n"	
		return f"**Query: {wiki}** **\n\nArticle Name:** *{howtoto.title}* ```\n{howtos}```"

class Random(commands.Cog):
	def __init__(self, bot):self.bot: commands.Bot = bot; self.start_time = datetime.now()

	@cog_ext.cog_slash(name='httpcat',description='Find some httpcats!',options=[create_option(name="error",description="Get a cat with selected error code, or get a random one!",option_type=3,required=False)])
	async def httpcat(self,ctx:SlashContext,error:int = None): await httpscat(ctx,error)

	@commands.command()
	async def httpcat(self,ctx,error:int = None): await httpscat(ctx,error)



	@cog_ext.cog_slash(name='uptime',description='Check the bot uptime')
	async def uptime(self,ctx:SlashContext): await timeup(ctx,self.start_time)

	@commands.command(aliases=["up"])
	async def uptime(self,ctx): await timeup(ctx,self.start_time)


	@cog_ext.cog_slash(name='wikihow',description='Parse through wikihow articles',options=[create_option(name="query",description="WikiHow search query.",option_type=3,required=True)])
	async def wikihowsh(self,ctx:SlashContext,query):
		components = [create_actionrow(create_button(style=ButtonStyle.red,emoji="🗑️",custom_id="d"))]
		message = await ctx.send(await whs(query),components=components)
		button_ctx = await wait_for_component(client=self.bot,components=components)
		if button_ctx.custom_id == "d":
			await message.delete()

	@commands.command(aliases=["wh"])
	async def wikihow(self,ctx,*,wiki):
		delwh=[Button(emoji='🗑️', style=ButtonStyle.red, custom_id='d')]
		message = await ctx.send(content=await whs(wiki),components=delwh)
		try: 
			delbtn = await self.bot.wait_for('button_click',check=lambda inter: inter.message.id == message.id, timeout=120)
			cmdlogger.info("WikiHow query deleted")
		except asyncio.TimeoutError: 
			await message.reply("Delete timed out")
			for row in delwh: row.disable_components()
		if delbtn.custom_id == "d":
			await message.delete()

	@cog_ext.cog_slash(name='braille',description='Translate english into braille. ⠞⠗⠁⠝⠎⠅⠁⠞⠑ ⠑⠝⠛⠅⠊⠎⠓ ⠊⠝⠞⠕ ⠃⠗⠁⠊⠅⠅⠑.',options=[create_option(name="english",description="English text to be translated into braille",option_type=3,required=True)])
	async def braille(self,ctx:SlashContext,*,english): await brr(ctx,english)

	@commands.command()
	async def braille(self,ctx,*,english): await brr(ctx,english)
	
	@commands.command()
	async def restart(self,ctx):
		if ctx.author.id == 454356237614841870:
			logger.warning("Restarting Bot"); await ctx.send("Restarting")
			python = sys.executable; os.execl(python, python, *sys.argv)

def setup(bot: commands.Bot):
	cmdlogger.info("Loading Random")
	bot.add_cog(Random(bot))
