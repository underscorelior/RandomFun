
import discord
from datetime import datetime

async def erremb(bot, ctx,error):
	erremb = discord.Embed(title="We have faced an error:" ,description=error ,color=0xd62d2d)
	erremb.set_footer(text=f"If you think this is wrong, please dm {(bot.get_user(454356237614841870))}")
	erremb.timestamp = datetime.utcnow()
	return await ctx.reply(embed=erremb)
async def toembed(timeout):
	toembed = discord.Embed(title="Timed Out:" ,description=timeout ,color=0xd62d2d)
	toembed.timestamp = datetime.utcnow()
	return toembed
async def toembedt(timeout,thmb):
	toembed = discord.Embed(title="Timed Out:" ,description=timeout ,color=0xd62d2d).set_thumbnail(url=thmb)
	toembed.timestamp = datetime.utcnow()
	return toembed