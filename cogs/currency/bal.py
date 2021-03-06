from __future__ import annotations

import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext	
from utils import getbal
#add markets, making stocks, making coins, etc
#mining with random math problems to get some coins

async def balemb(ctx, user, bal):
	balembed = discord.Embed(title=f"{user}'s balance",description=bal)
	balembed.set_author(name=user, icon_url=user.avatar_url)
	balembed.timestamp = datetime.datetime.utcnow()
	return await ctx.send(embed=balembed)


class Bal(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	@cog_ext.cog_slash(
		name='bal',
		description='Check a users\'s balance!',
		guild_ids=[566694134212198481])
	async def bal(self, ctx:SlashContext, *, user: discord.User = None):
		await ctx.defer()
		user = user or ctx.author
		balamt = getbal(str(user.id))
		await balemb(ctx,user,balamt)
		

def setup(bot: commands.Bot):
	print("Loading Bal")
	bot.add_cog(Bal(bot))
