import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils import permcheck
from utils import cmdlogger

async def roleinfoemb(ctx, role):
	if str(role.color) == "#000000":
		clr = 0x8F4088
		rclr = "None"
	else:
		clr = int(hex(int((str(role.color)).replace("#", ""), 16)), 0)
		rclr = role.color
	rinfemb = discord.Embed(title=f"{role.name}", description=f"💳 ID: {role.id} \n<:MENTION:925680840602681344> Mention: {role.mention}", color=clr)
	rcrts = str((role.created_at).timestamp()).split('.')[0]
	rmemm = ""
	for member in role.members:
		rmemm += f"{member.mention} "
	rinfemb.add_field(name="Info",value=f"📅 Created At: {rcrts} \n🎨 Color: {rclr} \n🔧 Permissions: \n```{await permcheck(int(role.permissions.value))}``` \n👥 Members: {rmemm}")
	rinfemb.timestamp = datetime.datetime.utcnow()
	return await ctx.send(embed=rinfemb)
class RoleInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='roleinfo',description='Check a role\'s info!')
	async def roleinfo(self,ctx:SlashContext,role: discord.Role):
		await ctx.defer()
		await roleinfoemb(ctx, role)	
		
def setup(bot: commands.Bot):
	cmdlogger.info("Loading RoleInfo")
	bot.add_cog(RoleInfo(bot))
