import discord
import discord_slash
from discord.ext import commands
from discord_components import DiscordComponents

import os
import time
import aiohttp
import logging
from dotenv import load_dotenv
from loghooks import WebhookHandler

load_dotenv()
whurl = os.getenv("WHURL")

bot = commands.Bot(
	command_prefix="rf!",
	intents=discord.Intents.all(),
	allowed_mentions=discord.AllowedMentions(everyone=False),
	status=discord.Status.dnd,
	activity=discord.Game("rm -rf —no-preserve-root /")
)
handler = WebhookHandler(
    webhook_url = whurl,
    session = aiohttp.ClientSession()
)

slash = discord_slash.SlashCommand(bot, sync_commands=True)

@bot.event 
async def on_ready(): 
	print(f"Logged in as {bot.user.name} at {time.ctime()}")
	DiscordComponents(bot)
	
# bot.load_extension("utils.errorhandling")
bot.load_extension('jishaku')
bot.load_extension("cog_reloader")

extfilenames = (
	'games',
	'random',
	# 'currency',
	'info',
	# 'media',
	# 'music',
	'minecraft'
)
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
handler.setLevel(logging.INFO)

for extfn in extfilenames:
	for filename in os.listdir(f'./cogs/{extfn}'):
		if filename.endswith('.py'):
			try: 
				bot.load_extension(f"cogs.{extfn}.{filename[:-3]}")
			except Exception as e: 
				print(f'Failed to load extension {extfn}.{filename}. \n{e}')


if __name__ == "__main__":
	load_dotenv()
	token = os.getenv("TOKEN")
	bot.run(token)
