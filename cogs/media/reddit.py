import discord, datetime, time, aiohttp, asyncio, random
from discord.ext import commands
from random import randint
from random import choice
from urllib.parse import quote_plus
from collections import deque
import os
import ast
import inspect
import io
import textwrap
from utils import cmdlogger
import traceback
from contextlib import redirect_stdout

acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()

class reddit(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ctx: commands.Context
	async def getSub(self,ctx, sub):
		"""Get stuff from requested sub"""
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://www.reddit.com/r{sub}/hot.json?limit=100") as response:
				request = await response.json()

		attempts = 1	
		while attempts < 5:
			if 'error' in request:
				cmdlogger.info("failed request {}".format(attempts))
				await asyncio.sleep(2)
				async with aiohttp.ClientSession() as session:
					async with session.get(f"https://www.reddit.com/r/{sub}/hot.json?limit=100") as response:
						request = await response.json()
				attempts += 1
			else:
				index = 0

				for index, val in enumerate(request['data']['children']):
					if 'url' in val['data']:
						url = val['data']['url']
						urlLower = url.lower()
						accepted = False
						for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
							if v in urlLower:
								accepted = True
						if accepted:
							if url not in memeHistory:
								memeHistory.append(url)  #add the url to the history, so it won't be posted again
								if len(memeHistory) > 63: #limit size
									memeHistory.popleft() #remove the oldest

								break #done with this loop, can send image
				await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
				return
		await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

		
	@commands.command()
	async def meme(self, ctx):
		memelist=["memes","dankmemes","me_irl"]
		mmls=random.choice(memelist)
		await self.getSub(ctx,mmls)

	@commands.command()
	async def randreddit(self, ctx):
		rrlist=['memes', 'softwaregore', 'technicallythetruth','comedycemetery','blursedimages','comedyheaven','onejob','ihadastroke','boottobig']
		rrand=random.choice(rrlist)
		await self.getSub(ctx,rrand)
		cmdlogger.info(rrand)

	@commands.command()
	async def games(self, ctx):
		glist=['minecraft','terraria','gaming','breath_of_the_wild','zelda','overwatch','pokemon','amongus']
		grand=random.choice(glist)
		await self.getSub(ctx,grand)

	@commands.command()
	async def reddit(self,ctx,search):
		await self.getSub(ctx,search)

def setup(bot):
	cmdlogger.info("Loading Reddit")
	bot.add_cog(reddit(bot))
