import datetime
import asyncio
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import youtube_dl
import logging
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
	'format': 'bestaudio/best',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = ""

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['title'] if stream else ytdl.prepare_filename(data)
		return filename
 
class Music(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot

	@cog_ext.cog_slash(name='music',description='Play music from youtube or spotify!',guild_ids=[566694134212198481])
	async def music(self,ctx:SlashContext,url):
		await ctx.defer()	

		if not ctx.author.voice:
			await ctx.send(f"{ctx.author.name} is not connected to a voice channel")
		else:
			channel = ctx.author.voice.channel
			await channel.connect()
			server = ctx.guild
			voice_channel = server.voice_client
			filename = await YTDLSource.from_url(url)
			await ctx.send('**Now playing:** {}'.format(filename))
			voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
			


	@commands.command()
	async def gtfo(self,ctx):
		for x in self.bot.voice_clients:
			if (x.guild == ctx.guild):
				await ctx.send("RF hath been gtfo'd")
				return await x.disconnect()

					
def setup(bot: commands.Bot):
	logger.info("Loading Music")
	bot.add_cog(Music(bot))
