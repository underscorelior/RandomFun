from utils import cmdlogger
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
# word detection from replying to a message
class Wordle(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	# @cog_ext.cog_slash(name='userinfo',description='Check another users info!',guild_ids=[566694134212198481]) #,options=[create_option(name="user",description="Mention the user you want the info for.",option_type=6,required=False)]
	# async def userinfo(self,ctx:SlashContext,user: discord.Member = None):
	# 	await ctx.defer()
	# 	await userinfoemb(ctx,user)

	global wordlewords
	wordlewords="balls"

	@commands.command()
	async def wordle(self,ctx,word: str):
		wordeee=""
		if word and len(word) == 5:
			with open('data/wordlewords.txt', 'r') as f:
				words = f.read()
				if word.lower() in words:
					wordss = word.lower()
					for e in range(len(word.lower())):
						if wordss[e] in wordlewords:
							if word[e] == wordlewords[e]:
								wordeee += "🟩"
							elif wordss[e] in wordlewords:
								wordeee += "🟨"
						else:
							wordeee += "🟥"
					await ctx.send(wordeee)
				else:
					await ctx.send("Invalid")
		else:
			await ctx.send("Please use a 5 letter word!")
		

def setup(bot: commands.Bot):
	cmdlogger.info("Loading Wordle")
	bot.add_cog(Wordle(bot))
