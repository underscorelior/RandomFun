import datetime
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils import cmdlogger
import aiohttp
from dotenv import load_dotenv
import os
import asyncio
from discord.errors import Forbidden
load_dotenv()
api_key = os.getenv("HYPAPI")
demo = "💀"
bemo = "🏡"
aemo = "👽"
async def mainemb(ctx,zombdata,username):
	acc = zombdata["bullets_hit_zombies"]/zombdata["bullets_shot_zombies"]
	if acc == 1.00:
		acc = f"100% /wdr {username} aimbot"
	if acc == 0.00:
		acc = "0% stop playing this game u cant aim"
	else:
		acc = round(acc,2)
		acc = str(acc).replace("0.","")
		acc = acc+"%"
	hsacc = zombdata["headshots_zombies"]/zombdata["bullets_hit_zombies"]
	if hsacc == 1.00:
		hsacc = f"100%"
	if hsacc == 0.00:
		hsacc = "0%"
	else:
		hsacc = round(hsacc,2)
		hsacc = str(hsacc).replace("0.","")
		hsacc = hsacc+"%"
	zomemb=discord.Embed(title="{}'s zombies stats".format(username),description="[API](https://api.hypixel.net)", color=0x1f8921)
	if "zombie_kills_zombies" in zombdata.keys():
		zomemb.add_field(name="Total Kills 🗡️",value=zombdata["zombie_kills_zombies"])
	if "players_revived_zombies" in zombdata.keys():
		zomemb.add_field(name="Players Revived 💊",value=zombdata["players_revived_zombies"])
	if "doors_opened_zombies" in zombdata.keys():
		zomemb.add_field(name="Doors Opened 🚪",value=zombdata["doors_opened_zombies"])
	if "windows_repaired_zombies" in zombdata.keys():
		zomemb.add_field(name="Windows Repaired 🧱",value=zombdata["windows_repaired_zombies"])
	if "bullets_shot_zombies" in zombdata.keys() and "bullets_hit_zombies" in zombdata.keys():
		zomemb.add_field(name="Accuracy 🏹",value=acc)
	if "headshots_zombies" in zombdata.keys():
		zomemb.add_field(name="Headshots 🎯",value=f'{zombdata["headshots_zombies"]}   {hsacc}')
	if "total_rounds_survived_zombies" in zombdata.keys():
		zomemb.add_field(name="Total Rounds Survived 🏆",value=zombdata["total_rounds_survived_zombies"])
	if "wins_zombies" in zombdata.keys():
		zomemb.add_field(name="Total Wins 🏁",value=zombdata["wins_zombies"])
	if "deaths_zombies" in zombdata.keys():
		zomemb.add_field(name="Deaths 💀",value=zombdata["deaths_zombies"])
	if  "times_knocked_down_zombies" in zombdata.keys():
		zomemb.add_field(name="Times Downed 🚫",value=zombdata["times_knocked_down_zombies"])
	zomemb.set_thumbnail(url=f"https://minotar.net/helm/{username}/100.png")
	zomemb.set_footer(text=f"💀 - Dead End \n🏡 - Bad Blood \n👽 - Alien Arcadium")
	return await ctx.send(embed=zomemb)

class ZombiesHYP(commands.Cog):
	def __init__(self, bot):
		self.bot: commands.Bot = bot
	@commands.command(aliases=['zomb']) #main, deadend = zombie, badblood = mansion/house, alien arcadium = alien, kill stats = knife  
	async def zombies(self,ctx, username):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://api.hypixel.net/player?key={api_key}&name={username}") as r:
				data = await r.json()
		if data["player"] is not None:
			zombdata = data["player"]["stats"]["Arcade"]
			if "deaths_zombies" in zombdata.keys():
				message = await mainemb(ctx, zombdata, username)
				await message.add_reaction(demo)
				await message.add_reaction(bemo)
				await message.add_reaction(aemo)
				def check(reaction, user):
					return user == ctx.author and str(reaction.emoji) == reaction.emoji
				try:
					reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
				except asyncio.TimeoutError:
					try:
						await message.clear_reactions()
					except Forbidden:
						pass
				else:
					if reaction.emoji == '💀':
						try:
							await message.clear_reactions()
						except Forbidden:
							pass
						dezombkill=discord.Embed(title="{}'s Dead End kill stats".format(username),description=f"Total Kills - {zombdata['zombie_kills_zombies']}", color=0x894f1f)
						if "wolf_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Wolves 🐺",value=zombdata["wolf_zombie_kills_zombies"])
						if "basic_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Basic Zombies 🧟",value=zombdata["basic_zombie_kills_zombies"])
						if "empowered_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Empowered Zombies 🪓",value=zombdata["empowered_zombie_kills_zombies"])
						if "pig_zombie_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Pig Zombies 🐖",value=zombdata["pig_zombie_zombie_kills_zombies"])
						if "tnt_baby_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Tnt Baby Zombies 🧨",value=zombdata["tnt_baby_zombie_kills_zombies"])
						if "tnt_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Bombie 💣",value=zombdata["tnt_zombie_kills_zombies"])
						if "magma_zombie_kills_zombies" in zombdata.keys() and "magma_cube_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Magma Zombies 💥",value=zombdata["magma_zombie_kills_zombies"]+ zombdata["magma_cube_zombie_kills_zombies"])
						if "fire_zombie_kills_zombies" in zombdata.keys() and "blaze_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Blaze Zombies 🕯",value=zombdata["fire_zombie_kills_zombies"]+ zombdata["blaze_zombie_kills_zombies"])
						if "inferno_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name = "Inferno 🔥",value=zombdata["inferno_zombie_kills_zombies"])
						if "fire_zombie_kills_zombies" in zombdata.keys() and "blaze_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Skelefish Zombies 🦴",value=zombdata["skelefish_zombie_kills_zombies"] + zombdata["silverfish_zombie_kills_zombies"])
						if "ender_zombie_kills_zombies" in zombdata.keys() and "endermite_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Enderman Zombies ☄️",value=zombdata["ender_zombie_kills_zombies"]+ zombdata["endermite_zombie_kills_zombies"])
						if "guardian_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Guardian Zombies 🐟",value=zombdata["guardian_zombie_kills_zombies"])
						if "broodmother_zombie_kills_zombies" in zombdata.keys():
							dezombkill.add_field(name="Broodmother 🕸️",value=zombdata["broodmother_zombie_kills_zombies"])
						dezombkill.set_thumbnail(url=f"https://minotar.net/helm/{username}/100.png")
						await ctx.send(embed=dezombkill)
					else:
						await ctx.send("`{}` has never played Zombies ".format(username))
		else:
			await ctx.send("`{}` is not a valid username".format(username))

def setup(bot: commands.Bot):
	cmdlogger.info("Loading ZombiesHYP")
	bot.add_cog(ZombiesHYP(bot))
