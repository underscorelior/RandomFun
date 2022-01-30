from datetime import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils import cmdlogger
import utils
import psutil
import os
import platform
def conv(t):
	return str((t).timestamp()).split('.')[0]
async def botinfemb(ctx,bot,start_time):
	binfemb = discord.Embed(
		title="Bot Info", 
		description=f"[Invite Bot](https://discord.com/oauth2/authorize?client_id=708083169831682110&permissions=1551232064&scope=bot%20applications.commands \"Invite Link\") ‖ [Server](https://www.discord.gg/ \"Server\") ‖ [Website](https://rf.underscore.wtf/ \"Webksite\")\n\n Discord bot made by {bot.get_user(454356237614841870)}.\n I was created at <t:{conv(bot.get_user(708083169831682110).created_at)}:F> \nI have been online since <t:{conv(start_time)}:F> (<t:{conv(start_time)}:R>)\n I am running on {platform.platform()}",
		color=0xbedefa
	)
	binfemb.add_field(name="Statistics",value=f"Guilds: {len(bot.guilds)} \nUsers: {len(bot.users)}")
	binfemb.add_field(name="System",value=f"CPU: {round(psutil.cpu_percent(),1)}/100.0% \nMemory: {psutil.virtual_memory().percent}/100.0& \nStorage: {psutil.disk_usage('/')}")
	binfemb.timestamp = datetime.utcnow()
	return await ctx.send(embed=binfemb)
class RoleInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
		self.start_time = datetime.now()

	@cog_ext.cog_slash(name='botinfo',description='Check the bot\'s info!', guild_ids=[566694134212198481])
	async def botinfo(self,ctx:SlashContext):
		await ctx.defer()
		await botinfemb(ctx,self.bot, self.start_time)	
	@commands.command(aliases=["bi"])
	async def botinfo(self,ctx):
		await botinfemb(ctx,self.bot, self.start_time)	
		
def setup(bot: commands.Bot):
	cmdlogger.info("Loading Botinfo")
	bot.add_cog(RoleInfo(bot))
