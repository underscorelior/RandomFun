import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils import cmdlogger, erremb
import json
import random
import finnhub
import asyncio
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

async def stockcd(ctx, bot, stock):
	if stock == None:
		with open('data/stocks.json') as fp:
			rstk = json.load(fp)
			stock = rstk[random.randint(0,len(rstk)-1)]
	finnhub_client = finnhub.Client(api_key="c7fs6daad3if3foe6ssg")
	prof = finnhub_client.company_profile2(symbol=stock)
	cost = finnhub_client.quote(symbol=stock)

	options = webdriver.ChromeOptions()
	options.headless = True
	driver = webdriver.Chrome(options=options)		
	try :
		print("1")
		emtitle = prof["name"]
		embed=discord.Embed(title=emtitle, description=prof["ticker"], color=0x5f5cff)
		embed.add_field(name="Close Price:", value=f"{'{:,}'.format(cost['c'])}")
		embed.add_field(name="Open Price:", value=f"{'{:,}'.format(cost['o'])}")
		embed.add_field(name="Highest Price in Previous Close:", value=f"{'{:,}'.format(cost['h'])}",inline=False)
		embed.add_field(name="Lowest Price in Previous Close:", value=f"{'{:,}'.format(cost['l'])}")
		embed.add_field(name="Aggregate Window:", value=f"<t:{cost['t']}:F> (<t:{cost['t']}:R>)",inline=False)
		embed.set_footer(text=f"{prof['country']} ‖ {prof['currency']}")
		embed.timestamp = datetime.datetime.utcnow()
		try:
			driver.get(f'https://www.tradingview.com/chart/?symbol={prof["exchange"].split(" ")[0]}%3A{stock}')
			asyncio.sleep(0.2)
			try:
				driver.find_element_by_class_name("button-qM2OSl9-").click()
			except NoSuchElementException or ElementNotInteractableException:
				pass
			driver.set_window_size(1280,720)                                                                                                             
			driver.find_element_by_class_name('chart-markup-table').screenshot('web_screenshot.png')

			driver.quit()
			myfile = discord.File('web_screenshot.png')
			embed.set_image(url="attachment://web_screenshot.png")
			await ctx.reply(file=myfile, embed=embed)
		except KeyError:
			await ctx.reply(embed=embed)
	except KeyError:
		print("2")
		try:
			print("3")
			emtitle = prof["ticker"]
		except KeyError:
			await erremb(bot, ctx,f"The following stock `{stock}` is Invalid or has missing information!")
			print("4")

class Stocks(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	
	@cog_ext.cog_slash(name='stocks',description='Check some info about a stock!',guild_ids=[566694134212198481])
	async def stockslash(self,ctx:SlashContext, stock = None):
		await ctx.defer()
		await stockcd(ctx, self.bot, stock)
	
	@commands.command(aliases=['stocks'])
	async def stock(self,ctx, stock = None):
		async with ctx.channel.typing():
			await stockcd(ctx, self.bot, stock)
			print("Ok")
		

		
		
def setup(bot: commands.Bot):
	cmdlogger.info("Loading Stocks")
	bot.add_cog(Stocks(bot))
