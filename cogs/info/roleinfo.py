from datetime import datetime
from utils import permcheck

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

async def roleinfoemb(ctx, role):
	if str(role.color) == "#000000": clr = 0x8F4088; rclr = "None"
	else: clr = int(hex(int((str(role.color)).replace("#", ""), 16)), 0); rclr = role.color

	rinfemb = discord.Embed(title=f"{role.name}", description=f"💳 ID: {role.id} \n<:MENTION:925680840602681344> Mention: {role.mention}", color=clr, timestamp = datetime.utcnow())
	rcrts = str((role.created_at).timestamp()).split('.')[0]
	rinfemb.add_field(name="Info",value=f"📅 Created At: <t:{rcrts}:F> \n🎨 Color: {rclr} \n🔧 Permissions: \n```{await permcheck(int(role.permissions.value))}``` \n👥 Members: {len(role.members)}")
	return await ctx.send(embed=rinfemb)

class RoleInfo(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='roleinfo',description='Check a role\'s info!',options=[create_option(name="role",description="Mention the role you want the info for.",option_type=8,required=True)])
	async def roleinfo(self,ctx:SlashContext,role):
		await ctx.defer()
		await roleinfoemb(ctx, role)
	
	@commands.command(aliases=["ri"])
	async def roleinfo(self,ctx, role: discord.Role):
		await roleinfoemb(ctx, role)
		
def setup(bot: commands.Bot):
	print("Loading RoleInfo")
	bot.add_cog(RoleInfo(bot))
