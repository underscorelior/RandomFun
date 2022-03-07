from utils import cmdlogger
import discord
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
# word detection from replying to a message
class Wordle(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	global wordlewords
	with open('data/wordlewords.txt', 'r') as f: wordlewords = random.choice(f.read().splitlines())

	@commands.command()
	async def wordle(self,ctx,wordi: str):
		word=wordi
		wordeee=""
		await ctx.send(wordlewords)
		if word and len(word) == 5:
			with open('data/wordlewords.txt', 'r') as f:
				wordss = word.lower()
				words = f.read()
				if wordss in words:
					for e in range(len(word)):
						if wordss[e] in wordlewords:
							if word[e] == wordlewords[e]: wordeee += "🟩"
							elif wordss[e] in wordlewords: wordeee += "🟨"
						else: wordeee += "🟥"
					await ctx.send(wordeee)
					if wordeee == "🟩🟩🟩🟩🟩": self.bot.reload_extension("cogs.games.wordle")
				else: await ctx.send("Invalid")
		else: await ctx.send("Please use a 5 letter word!")
		

def setup(bot: commands.Bot):
	cmdlogger.info("Loading Wordle")
	bot.add_cog(Wordle(bot))
