import discord
import discord_slash
from discord.ext import commands

import os
import time
from utils import logger
from dotenv import load_dotenv


bot = commands.Bot(command_prefix="rf!",intents=discord.Intents.all(),allowed_mentions=discord.AllowedMentions(everyone=False))
slash = discord_slash.SlashCommand(bot, sync_commands=True)

@bot.event 
async def on_ready(): 
	logger.info(f"Logged in as {bot.user.name} at {time.ctime()}"); await bot.change_presence(status=discord.Status.dnd,activity=discord.Game("rm -rf slash"))
	
bot.load_extension("utils.errorhandling")
bot.load_extension('jishaku')
bot.load_extension("cog_reloader")
extfilenames = (
	'games',
	'random',
	'currency',
	'info',
	'media',
	'music'
)
for extfn in extfilenames:
	for filename in os.listdir(f'./cogs/{extfn}'):
		if filename.endswith('.py'):
			try:
				bot.load_extension(f"cogs.{extfn}.{filename[:-3]}")
			except Exception as e:
				logger.error(f'Failed to load extension {extfn}.{filename}.')

load_dotenv()
token = os.getenv("TOKEN")
bot.run(token)