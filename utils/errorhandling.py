import discord
import sys
import traceback
from utils import logger
from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.on_command_error, "on_command_error")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return  # Don't interfere with custom error handlers

        error = getattr(error, "original", error)  # get original error

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(
                f"That command does not exist. Please use `{self.bot.command_prefix}help` for a list of commands."
            )

        if isinstance(error, commands.CommandError):
            return await ctx.send(
                f"Error executing command `{ctx.command.name}`: {str(error)}")

        await ctx.send(
            "An unexpected error occurred while running that command.")
        logger.warn("Ignoring exception in command {}:".format(ctx.command))
        logger.warn("\n" + "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__)))

def setup(bot: commands.Bot):
	logger.info("Loading Error")
	bot.add_cog(CommandErrorHandler(bot))
