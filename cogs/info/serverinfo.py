import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils import cmdlogger

async def serverinfoemb(ctx, guild):
	print("OK")
	if guild.description == None:
		udesc = "No description set"
	else:
		udesc = guild.description
	sinfemb = discord.Embed(title=f"{guild.name}", description=f"💳 ID: {guild.id} \nℹ️ Description: {udesc}", color=0x3465d9)

	sinfemb.add_field(name="Channels", value=f"#️⃣ Text: {len(guild.text_channels)} \n🔊 Voice: {len(guild.voice_channels)} \n🪢 Category: {len(guild.categories)}\n📢 Stages: {len(guild.stage_channels)}")

	sinfemst = 0
	sinfeman = 0
	for emoji in guild.emojis:
		if emoji.animated:
			sinfeman += 1
		else:
			sinfemst += 1
		
	sinfemb.add_field(name="Emojis", value=f"😀 Total: {len(guild.emojis)} \n😴 Static: {sinfemst} \n🎞️ Animated: {sinfeman} \n🔒 Limit: {guild.emoji_limit}")
	
	smemb = 0
	smemu = 0
	for member in ctx.guild.members:
		if member.bot:
			smemb += 1
		else:
			smemu += 1
	smaxmem = "{:,}".format(guild.max_members)
	sinfemb.add_field(name="Members",value=f"♾️ Total: {len(guild.members)} \n👤 Users: {smemu} \n🤖 Bots: {smemb} \n↕️ Limit: {smaxmem}",inline=True)

	smemon = 0
	smemid = 0
	smemdn = 0
	smemof = 0
	for member in guild.members:
		if str(member.status).lower() == "online":
			smemon += 1
		elif str(member.status).lower() == "idle":
			smemid += 1
		elif str(member.status).lower() == "dnd":
			smemdn += 1
		else:
			smemof += 1
	sinfemb.add_field(name="Member Statuses",value=f"<:ONLINE:920502834695389214> Online: {smemon} \n<:IDLE:920502844099018813> Idle: {smemid} \n<:DND:920502802680274945> Dnd: {smemdn} \n<:OFF:920502852315664405> Offline: {smemof}")

	scrts = str((guild.created_at).timestamp()).split('.')[0]
	if ctx.guild.premium_tier == 1:
		gbtr = "Boost Tier 1"
	if ctx.guild.premium_tier == 2:
		gbtr = "Boost Tier 2"
	if ctx.guild.premium_tier == 3:
		gbtr = "Boost Tier 3"
	else:
		gbtr = "No Boosts"
	sinfemb.add_field(name="Other",value=f"🏷️ Roles: {len(guild.roles)} \n📁 Filesize Limit: {guild.filesize_limit/1000} KB \n🔈Bitrate Limit: {guild.bitrate_limit/1000000} MB \n<:BOOST:925678571266125875> Boost Tier: {gbtr} / *Boosts: {guild.premium_subscription_count}*\n📅 Created At: <t:{scrts}:F> (<t:{scrts}:R>)")
	if guild.icon is not None: sinfemb.set_thumbnail(url=guild.icon_url)
	sinfemb.timestamp = datetime.datetime.utcnow()
	sjnts = str((guild.get_member(ctx.author.id).joined_at)).split(' ')[0]


	sinfemb.set_footer(text = f"⚙️ Owner: {guild.owner} ‖🌐 Region: {guild.region} ‖ {ctx.author} joined at {sjnts}")


	if guild.banner is not None: sinfemb.set_image(url=guild.banner_url)

	return await ctx.send(embed=sinfemb)
class ServerInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='serverinfo',description='Check the server\'s info!',guild_ids=[566694134212198481])
	async def userinfo(self,ctx:SlashContext):
		# await ctx.send("Bruh")
		await ctx.defer()
		guild = ctx.guild
		await serverinfoemb(ctx, guild)

	@commands.command(aliases=["si"])
	async def serverinfo(self,ctx):
		guild = ctx.guild
		await serverinfoemb(ctx, guild)
		
		

def setup(bot: commands.Bot):
	cmdlogger.info("Loading ServerInfo")
	bot.add_cog(ServerInfo(bot))
