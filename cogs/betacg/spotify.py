import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import io, aiohttp
from utils import cmdlogger

async def spotifyemb(ctx, member):
	spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
	if not spotify:
		return await ctx.send(f"{member} is not listening or connected to Spotify.")
	params = {
		'title': spotify.title,
		'cover_url': spotify.album_cover_url,
		'duration_seconds': spotify.duration.seconds,
		'start_timestamp': spotify.start.timestamp(),
		'artists': spotify.artists
	}
	async with aiohttp.ClientSession() as session:
		async with session.get('https://api.jeyy.xyz/discord/spotify', params=params) as response:
			buf = io.BytesIO(await response.read())
			artists = ', '.join(spotify.artists)
	await ctx.send(f"> {member} is listening to {spotify.title} by {artists}", file=discord.File(buf, 'spotify.png'))
class Spotify(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='spotify',description='Check someone\'s spotify listening!',guild_ids=[566694134212198481])
	async def spotify(self,ctx:SlashContext, member: discord.Member = None):
		await ctx.defer()
		member = member or ctx.author
		await spotifyemb(ctx, member)	
		spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
		if not spotify:
			return await ctx.send(f"{member} is not listening or connected to Spotify.")
		params = {
			'title': spotify.title,
			'cover_url': spotify.album_cover_url,
			'duration_seconds': spotify.duration.seconds,
			'start_timestamp': spotify.start.timestamp(),
			'artists': spotify.artists
		}
		async with aiohttp.ClientSession() as session:
			async with session.get('https://api.jeyy.xyz/discord/spotify', params=params) as response:
				buf = io.BytesIO(await response.read())
				artists = ', '.join(spotify.artists)
				await ctx.send(f"> {member} is listening to {spotify.title} by {artists}", file=discord.File(buf, 'spotify.png'))
		
def setup(bot: commands.Bot):
	cmdlogger.info("Loading Spotify")
	bot.add_cog(Spotify(bot))
