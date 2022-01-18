import discord
import discord_slash
from discord.ext import commands
import time
import os
from utils import logger
from dotenv import load_dotenv



bot = commands.Bot(command_prefix="rf!",intents=discord.Intents.all(),allowed_mentions=discord.AllowedMentions(everyone=False))
slash = discord_slash.SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
	logger.info(f"Logged in as {bot.user.name} at {time.ctime()}"); await bot.change_presence(status=discord.Status.dnd,activity=discord.Game("rm -rf slash"))
	

bot.load_extension("utils.errorhandling")
initial_extensions = (
	'cogs.games.rps',
	'cogs.random.random',
	'cogs.random.calculator',
	'cogs.currency.blackjack',
	'cogs.info.userinfo',
	'cogs.info.serverinfo',
	'cogs.info.roleinfo',
	'cogs.random.spotify',
	'cogs.media.reddit',
	'cogs.music.music',
	'cogs.currency.bal',
	'cogs.random.stocks',
	
)	
for extension in initial_extensions:
	try:
		bot.load_extension(extension)
	except Exception as e:
		logger.error(f'Failed to load extension {extension}.')

bot.load_extension('jishaku')
bot.load_extension("cog_reloader")

load_dotenv()
token = os.getenv("TOKEN")


bot.run(token)