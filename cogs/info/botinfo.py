import sys
import math
import psutil
import pathlib
import os, os.path
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

proc = psutil.Process()

def natural_size(size_in_bytes: int):
    units = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')

    power = int(math.log(size_in_bytes, 1024))

    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"
mem = proc.memory_full_info()
def lines():
	total = 0
	file_amount = 0
	ENV = "env"
	for path, _, files in os.walk("."):
		for name in files:
			file_dir = str(pathlib.PurePath(path, name))
			if not name.endswith(".py") or ENV in file_dir:
				continue
			file_amount += 1
			with open(file_dir, "r", encoding="utf-8") as file:
				for line in file:
					if not line.strip().startswith("#") or not line.strip():
						total += 1
	return total, file_amount
def char():
	character_count = 0
	ENV = "env"
	for path, _, files in os.walk("."):
		for name in files:
			file_dir = str(pathlib.PurePath(path, name))
			if not name.endswith(".py") or ENV in file_dir:
				continue
			with open(file_dir, "r", encoding="utf-8") as file:
				character_count += len(file.read())
	return character_count
def conv(t):
	return str((t).timestamp()).split('.')[0]
async def botinfemb(ctx,bot,start_time):
	binfemb = discord.Embed(
		title="Bot Info", 
		description=f"""[Invite Bot](https://discord.com/oauth2/authorize?client_id=708083169831682110&permissions=1551232064&scope=bot%20applications.commands \"Invite Link\") **‖** [Server](https://discord.gg/UyXARxeSBZ \"Server\") **‖** [Website](https://rf.underscore.wtf/ \"Website\")\n
			Discord bot made by {bot.get_user(454356237614841870)}.\n I was created on <t:{conv(ctx.me.created_at)}:F>
			I have been online since <t:{conv(start_time)}:F> (<t:{conv(start_time)}:R>)\n I am in `{len(bot.guilds)}` Guilds and I can see `{len(bot.users)}` Users.\n I have `{len(bot.commands)}` commands.""",
		color=0xbedefa)
	binfemb.add_field(name="System Information",value=f"Operating System: `{sys.platform}` \nCPU: `{round(psutil.cpu_percent(),1)}%` \nMemory: `{psutil.virtual_memory().percent}%` (`{natural_size(mem.rss)}`) \nStorage: `{psutil.disk_usage('/').percent}%` \nPython Version: `{(sys.version).split(' ') [0]}`")
	binfemb.add_field(name="Files",value=f"File Count: `{lines()[1]}` \nLine Count: `{lines()[0]}` \nCharacter Count: `{char()}`")
	binfemb.set_footer(text=f"Latency: {round(bot.latency*1000, 2)}ms ‖ ID: {ctx.me.id}")
	binfemb.timestamp = datetime.utcnow()
	binfemb.set_thumbnail(url=ctx.me.avatar_url)
	return await ctx.send(embed=binfemb)
class BotInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.start_time = datetime.now()

	@cog_ext.cog_slash(name='botinfo',description='Check the bot\'s info!')
	async def botinfo(self,ctx:SlashContext):
		await ctx.defer()
		await botinfemb(ctx,self.bot, self.start_time)	
	@commands.command(aliases=["bi", "info", "stats"])
	async def botinfo(self,ctx):
		await botinfemb(ctx,self.bot, self.start_time)	
		
def setup(bot: commands.Bot):
	print("Loading Botinfo")
	bot.add_cog(BotInfo(bot))
