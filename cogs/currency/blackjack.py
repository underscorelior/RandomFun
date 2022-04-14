import asyncio
import random
import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from utils import getbal, save

class BJ(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='blackjack',description='Gamble away all of your money, or win the jackbot!',guild_ids=[566694134212198481])
	async def blackjack(self,ctx:SlashContext,bet:int = 100):
		from utils import getbal
		await ctx.defer()
		money = getbal(ctx.author.id)
		if abs(bet) != bet:
			await ctx.send("You cannot bet a negative amount!",hidden=True)
			return
		if bet > money:
			await ctx.send("You are betting money you don't have!",hidden=True)
			return
		components = [create_actionrow(create_button(style=ButtonStyle.blue,label="Hit",custom_id="h"),create_button(style=ButtonStyle.gray,label="Stand",custom_id="s"))]
		dealer_draws = 1
		player_cards = random.randint(1,10) + random.randint(1,10)
		dealer_cards = random.randint(1,10) + random.randint(1,10)
		embed = discord.Embed(title=f"Blackjack for <:RFCoin:917313958489243678>{bet}",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
		message = await ctx.send(embed=embed,components=components)
		while player_cards < 21:
			button_ctx = await wait_for_component(client=self.bot,components=components)
			if button_ctx.custom_id == "h":
				player_cards += random.randint(1,10)
			elif button_ctx.custom_id == "s":
				while dealer_cards <= 17:
					dealer_cards += random.randint(1,10)
					dealer_draws += 1
			embed = discord.Embed(title=f"Blackjack for <:RFCoin:917313958489243678>{bet}",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
			await message.edit(embed=embed)
			if player_cards > 21:
				await message.edit(content=f"You lose! -<:RFCoin:917313958489243678>{bet}.",embed=None)
				win = -1
				break
			if dealer_cards > 21 or (dealer_cards >= 17 and player_cards > dealer_cards):
				await message.edit(content=f"You win! +<:RFCoin:917313958489243678>{bet}.",embed=None)
				win = 1
				break
			if dealer_cards == 21 and (player_cards == dealer_cards):
				await message.edit("It's a draw!")
				return
		await ctx.send(content=f"You now have a total of <:RFCoin:917313958489243678>{money + (bet * win)}.",embed=None,hidden=True)
		save(money + (bet * win),ctx.author.id)

def setup(bot: commands.Bot):
	print("Loading BJ")
	bot.add_cog(BJ(bot))
