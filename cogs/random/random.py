import random
from datetime import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from pywikihow import search_wikihow
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from utils import cmdlogger
import aiohttp
import os
import sys
# import hypixel

def format_seconds(time_seconds):
	"""Formats some number of seconds into a string of format d days, x hours, y minutes, z seconds"""
	seconds = time_seconds
	hours = 0
	minutes = 0
	days = 0
	while seconds >= 60:
		if seconds >= 60 * 60 * 24:
			seconds -= 60 * 60 * 24
			days += 1
		elif seconds >= 60 * 60:
			seconds -= 60 * 60
			hours += 1
		elif seconds >= 60:
			seconds -= 60
			minutes += 1

	return f"{days}d {hours}h {minutes}m {seconds}s"
async def mcserver(ip: str) -> dict:
	async with aiohttp.ClientSession(trust_env=True) as session:
		async with session.get(f'https://api.mcsrvstat.us/2/{ip}', ssl=False) as response:
			return await response.json()
class Random(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.start_time = datetime.now()

	@cog_ext.cog_slash(name='httpcat',description='Find some httpcats!')
	async def httpcat(self,ctx:SlashContext,error:int = None):
		httplist =[100,101,102,200,201,202,203,204,206,207,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,420,421,422,423,424,425,426,429,431,444,450,451,497,498,499,500,501,502,503,504,506,507,508,509,510,511,521,523,525,599]
		if error == None:  
			error = random.choice(httplist)
		await ctx.send(f"https://http.cat/{error}.jpg")



	@cog_ext.cog_slash(name='uptime',description='Check the bot uptime')
	async def uptime(self,ctx:SlashContext):
		uptime_seconds = round((datetime.now() - self.start_time).total_seconds())
		embed = discord.Embed(title="Uptime", description=format_seconds(uptime_seconds),color=0x2ab76f)
		embed.timestamp = datetime.utcnow()
		try:
			await ctx.send(embed=embed)
		except discord.HTTPException:
			await ctx.send(f"Current uptime: {format_seconds(uptime_seconds)}")



	@cog_ext.cog_slash(name='wikihow',description='Parse through wikihow articles')
	async def wikihow(self,ctx:SlashContext,wiki:str):
		howtos = ""
		max_results = 1
		how_tos = search_wikihow(wiki, max_results)
		howtoto =  how_tos[0]
		for step in range(len(howtoto.steps)):
			strep = howtoto.steps[step]
			howtos = howtos + str(strep.number) + " - " + strep.summary + "\n"
		components = [create_actionrow(create_button(style=ButtonStyle.red,emoji="🗑️",custom_id="h"))]
		message = await ctx.send(f"**Query: {wiki}** **\n\nArticle Name:** *{howtoto.title}* ```\n{howtos}```",components=components)
		button_ctx = await wait_for_component(client=self.bot,components=components)
		if button_ctx.custom_id == "h":
			await message.delete()
	

	@cog_ext.cog_slash(name='braille',description='Translate english into braille. ⠞⠗⠁⠝⠎⠅⠁⠞⠑ ⠑⠝⠛⠅⠊⠎⠓ ⠊⠝⠞⠕ ⠃⠗⠁⠊⠅⠅⠑.')
	async def braille(self,ctx:SlashContext,english):
		await ctx.send(f'English: {english} \nBraille: {(str(english).lower()).replace("a", "⠁").replace("b", "⠃").replace("c", "⠉").replace("d", "⠙").replace("e", "⠑").replace("f", "⠋").replace("g", "⠛").replace("h", "⠓").replace("i", "⠊").replace("j", "⠚").replace("k", "⠅").replace("l", "⠅").replace("m", "⠍").replace("n", "⠝").replace("o", "⠕").replace("p", "⠏").replace("q", "⠟").replace("r", "⠗").replace("s", "⠎").replace("t", "⠞").replace("u", "⠥").replace("v", "⠧").replace("w", "⠺").replace("x", "⠭").replace("y", "⠽").replace("z", "⠵")}')

	@commands.command()
	async def restart(self, ctx):
		if ctx.author.id == 454356237614841870:
			await ctx.send("Restarting")
			python = sys.executable
			os.execl(python, python, * sys.argv)		

	@commands.command()
	async def server(self, ctx, ipo: str=None):
		data = await mcserver(ipo)
		if len(data['ip']) == 0:
			embed = discord.Embed(title="Error", description="""That server does not exist.""", color=0xff0000)
			await ctx.send(embed=embed)
			return
		# if data['online'] == False:
		# 	embed = discord.Embed(title="Error", description="""That server is currently offline.\nTrying to query a Minecraft: Bedrock Edition server? Try port 19132.""", color=0xff0000)
		# 	await ctx.send(embed=embed)
		# 	return
		hostname = data['hostname']
		ip = data['ip']
		port = data['port']
		vers = data['version']	
		motd = ''
		if isinstance(data['motd']['clean'], list):
			mot = '\n'.join(data['motd']['clean'])
		else:
			mot = data['motd']['clean']
		abc = mot.split('?')
		for strl in abc:
			if strl != ' ':
				strl = strl[1:]
			motd += strl
		if motd.replace(' ', '') == '':
			motd = "None"
		players = f"{data['players']['online']}/{data['players']['max']}"
		embed = discord.Embed(title=f"Information on {ipo}", color=0x748aad)
		embed.set_thumbnail(url=f'https://api.mcsrvstat.us/icon/{hostname}')
		embed.add_field(name="Hostname", value=hostname, inline=True)
		embed.add_field(name="IP", value=ip, inline=True)
		embed.add_field(name="Port", value=port, inline=True)
		embed.add_field(name="Version", value=vers, inline=True)
		embed.add_field(name="Players", value=players, inline=True)
		embed.add_field(name="MoTD", value=motd, inline=True)
		# embed.set_footer(text="Unofficial Hypixel Discord Bot - Server info retrieved from api.mcsrvstat.us.")
		await ctx.send(embed=embed)
	#stackoverflow

def setup(bot: commands.Bot):
	cmdlogger.info("Loading Random")
	bot.add_cog(Random(bot))
