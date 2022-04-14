import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import aiohttp
from dotenv import load_dotenv
import os
import asyncio
from discord.errors import Forbidden
async def mcserver(ip: str) -> dict:
	async with aiohttp.ClientSession(trust_env=True) as session:
		async with session.get(f'https://api.mcsrvstat.us/2/{ip}', ssl=False) as response:
			return await response.json()
class ServerMC(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

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

def setup(bot: commands.Bot):
	print("Loading ServerMC")
	bot.add_cog(ServerMC(bot))
