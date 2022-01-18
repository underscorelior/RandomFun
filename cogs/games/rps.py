import random
import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from utils import cmdlogger
beating_table = {
	'🪨': '📰',
	'✂️': '🪨',
	'📰': '✂️'
}

rpsl = ['✂️','🪨','📰']
async def rpsemb1(ctx,status,rpsuser,rpscom,color,message):
	rpsembed = discord.Embed(title="RPS",desc=status,color=color)
	rpsembed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
	rpsembed.add_field(name=status,value=f"You chose {rpsuser}; The bot chose {rpscom}.")
	rpsembed.timestamp = datetime.datetime.utcnow()
	await message.edit(embed=rpsembed)
async def rpsemb2(ctx,rpswin,rpswinchoice,rpslose,rpslosechoice,message):
	rpsembed = discord.Embed(title="RPS2",color=0x008080)
	rpsembed.add_field(name=f"{rpswin} won!; {rpslose} lost.",value=f"{rpswin} chose {rpswinchoice}; {rpslose} chose {rpslosechoice}.")
	rpsembed.timestamp = datetime.datetime.utcnow()
	await message.edit(embed=rpsembed)
async def rpstie(ctx,rpswin,rpswinchoice,rpslose,message):
	rpsembed = discord.Embed(title="RPS2",color=0x543853)
	rpsembed.add_field(name=f"{rpswin} tied with {rpslose}.",value=f"Chose: {rpswinchoice}")
	rpsembed.timestamp = datetime.datetime.utcnow()
	await message.edit(embed=rpsembed)
async def timeoutemb(ctx,message):
	timeoutembed = discord.Embed(title="Timed out",description="408 Request Timeout",color=0x961006)
	timeoutembed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
	timeoutembed.timestamp = datetime.datetime.utcnow()
	await message.edit(embed=timeoutembed,components=None)

class RPS(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name="RPS",description="Play a game of Rock Paper Scissors")
	async def rps_start(self, ctx: SlashContext,member : discord.Member = None):
		await ctx.defer()
		if member == None:
			startembed = discord.Embed(title="Use of RPS",color=0x263340)
			startembed.add_field(name="Press the buttons: ",value="🪨 for rock. \n📰 for paper . \n✂️ for scissors.")
			startembed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
			startembed.timestamp = datetime.datetime.utcnow()
			buttons = [create_button(emoji = "🪨",style=ButtonStyle.blue, custom_id = "🪨",disabled=False), create_button(emoji = "📰", style=ButtonStyle.green, custom_id = "📰",disabled=False), create_button(emoji = "✂️", style=ButtonStyle.red, custom_id = "✂️",disabled=False)]
			action_row = create_actionrow(*buttons)
			message = await ctx.send(embed=startembed,components=[action_row])
			button_ctx:ComponentContext = await wait_for_component(self.bot,components=action_row,check=lambda c_ctx:c_ctx.author == ctx.author or c_ctx.author == member)
			rpscom = random.choice(rpsl)
			
			if button_ctx.component['custom_id'] == rpscom:
				await rpsemb1(ctx,"Tie",button_ctx.component['custom_id'],rpscom,0xFF5E13, message)
				cmdlogger.info("tie")
			else:
				if button_ctx.component['custom_id'] == beating_table[rpscom]:
					await rpsemb1(ctx,"Win!",button_ctx.component['custom_id'],rpscom,0x008080, message)
					cmdlogger.info("win")
				else:
					await rpsemb1(ctx,"Lose.",button_ctx.component['custom_id'],rpscom,0x8c1c12, message)
					cmdlogger.info("lose")
		else:
			startembed = discord.Embed(title="Use of RPS",color=0x263340)
			startembed.add_field(name="Press the buttons: ",value="🪨 for rock. \n📰 for paper . \n✂️ for scissors.")
			startembed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
			startembed.timestamp = datetime.datetime.utcnow()
			buttons = [create_button(emoji = "🪨",style=ButtonStyle.blue, custom_id = "🪨",disabled=False), create_button(emoji = "📰", style=ButtonStyle.green, custom_id = "📰",disabled=False), create_button(emoji = "✂️", style=ButtonStyle.red, custom_id = "✂️",disabled=False)]
			action_row = create_actionrow(*buttons)
			message = await ctx.send(content = f"{ctx.author.mention} {member.mention}",embed=startembed,components=[action_row])
			button_ctx:ComponentContext = await wait_for_component(self.bot,components=action_row,check=lambda c_ctx:c_ctx.author == ctx.author or c_ctx.author == member)
			await button_ctx.send(f"Chosen {button_ctx.component['custom_id']}\nWaiting on other user",hidden=True)
			button_ctx_2:ComponentContext = await wait_for_component(self.bot,components=action_row,check=lambda c_ctx:(c_ctx.author == ctx.author or c_ctx.author == member) and c_ctx.author != button_ctx.author)
			await button_ctx_2.send(f"Chosen {button_ctx_2.component['custom_id']}",hidden=True)
			if button_ctx.component['custom_id'] == button_ctx_2.component['custom_id']:
				await rpstie(ctx,str(button_ctx.author),button_ctx.component['custom_id'],str(button_ctx_2.author),message)
				cmdlogger.info("tie")
			else:
				if button_ctx.component['custom_id'] == beating_table[button_ctx_2.component['custom_id']]:
					await rpsemb2(ctx,str(button_ctx.author),button_ctx.component['custom_id'],str(button_ctx_2.author),button_ctx_2.component['custom_id'],message)
					cmdlogger.info("win")
				else:
					await rpsemb2(ctx,str(button_ctx_2.author),button_ctx_2.component['custom_id'],str(button_ctx.author),button_ctx.component['custom_id'],message)
					cmdlogger.info("lose")

def setup(bot: commands.Bot):
	cmdlogger.info("Loading RPS")
	bot.add_cog(RPS(bot))
