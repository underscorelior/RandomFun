from datetime import datetime
from utils import permcheck, cmdlogger
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


async def userinfoemb(ctx,user): 
	if str(user.color) == "#000000": clr = 0x1AFFCF
	else: clr = int(hex(int((str(user.color)).replace("#", ""), 16)), 0)

	uinfemb = discord.Embed(title=f"{user.name}", description=f"💳 ID: {user.id}", color=clr, timestamp = datetime.utcnow()).set_thumbnail(url=user.avatar_url)

	if not user.nick: unick = f"{user.name} (No nick set)"
	if user.nick: unick = user.nick

	ustatdev = ""
	if str(user.desktop_status) != "offline":
		ustatdev += " [🖥️]"
	if str(user.mobile_status) != "offline":
		ustatdev += " [📱]"
	if str(user.web_status) != "offline":
		ustatdev += " [🌐]"
	if ustatdev == "":
		ustatdev = "None"
	
	if user.bot: userbot="Yes"
	else: userbot="No"


	uinfemb.add_field(name="General", value=f"✏️ Nickname: {unick} \n#️⃣ Discriminator: #{user.discriminator} \n<:DISCORD:925674003593580615> Client: {ustatdev} \n🤖 Bot: {userbot} **‖** <:MENTION:925680840602681344> Mention: {user.mention}")

	ustatem = ""
	if str(user.status).lower() == "online":
		ustatem = "<:ONLINE:920502834695389214>"
	elif str(user.status).lower() == "idle":
		ustatem = "<:IDLE:920502844099018813>"
	elif str(user.status).lower() == "dnd":
		ustatem = "<:DND:920502802680274945>"
	else: ustatem = "<:OFF:920502852315664405>"

	useract = discord.utils.find(lambda a: isinstance(a, discord.CustomActivity), user.activities)
	if useract != None:
		ustat = f"**{useract.emoji}** {useract.name}"
	else: ustat= "None"

	if discord.utils.find(lambda a: isinstance(a, discord.Game), user.activities) != None:
		ugame = discord.utils.find(lambda a: isinstance(a, discord.Game), user.activities)
		uact = f"Playing **{ugame.name}**"
	elif discord.utils.find(lambda a: isinstance(a, discord.Activity), user.activities) != None:
		usact = discord.utils.find(lambda a: isinstance(a, discord.Activity), user.activities)
		uact = f"Playing **{usact.name}**"
	elif discord.utils.find(lambda a: isinstance(a, discord.Spotify), user.activities) != None:
		ulisten = discord.utils.find(lambda a: isinstance(a, discord.Spotify), user.activities)
		uact = f"Listening to **{ulisten.name}**"
	else: uact="None"
		
	if discord.utils.find(lambda a: isinstance(a, discord.Spotify), user.activities) != None:
		uspotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), user.activities)
		uspot = f"**[{uspotify.title}](https://open.spotify.com/track/{uspotify.track_id} \"Spotify Link\")** by {uspotify.artist} on *{uspotify.album}*"
	else: uspot = "Not playing"

	uinfemb.add_field(name="Activity", value=f"{ustatem} ‖ Status: {ustat} \n🎮 Activity: {uact} \n<:SPOTIFY:925674981059338261> Spotify: {uspot}")

	urol = ""
	if user.roles is not None:
		for role in user.roles[1:]:
			urol = role.mention + " " + urol
	else: urol = "None"

	if user.voice == None:
		uvc = "Not in a VC"
	else: uvc = f"<#{user.voice.channel.id}>"

	uinfemb.add_field(name="Server", value=f"👤 Roles: {urol} \n🔧 Permissions: \n```{await permcheck(int(user.guild_permissions.value))}``` \n🎨 Color: {user.color} \n🔊 Voice: {uvc}", inline=False)


	ucrts = str((user.created_at).timestamp()).split('.')[0]
	ujnts = str((user.joined_at).timestamp()).split('.')[0]
	if user.premium_since == None:
		ubsts = "Not Boosting"
	else:
		ubst = str((user.premium_since).timestamp()).split('.')[0]
		ubsts = f"<t:{ubst}:F> (<t:{ubst}:R>"

	uinfemb.add_field(name="Other", value=f"👶 Account Created: <t:{ucrts}:F> (<t:{ucrts}:R>) \n➡️ Joined Server At: <t:{ujnts}:F> (<t:{ujnts}:R>) \n<:BOOST:925678571266125875> Boosting: {ubsts} \n👥 Mutual Servers: {len(user.mutual_guilds)}", inline=False)

	uinfemb.set_footer(text = ctx.author)

	return await ctx.send(embed=uinfemb)
class UserInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='userinfo',description='Check another users info!',guild_ids=[566694134212198481]) #,options=[create_option(name="user",description="Mention the user you want the info for.",option_type=6,required=False)]
	async def userinfo(self,ctx:SlashContext,user: discord.Member = None):
		await ctx.defer()
		await userinfoemb(ctx,user)

	
	@commands.command(aliases=["ui"])
	async def userinfo(self,ctx,user: discord.Member = None):
		user = user or ctx.author
		await userinfoemb(ctx,user)
		

def setup(bot: commands.Bot):
	cmdlogger.info("Loading Userinfo")
	bot.add_cog(UserInfo(bot))
