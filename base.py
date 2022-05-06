import discord
from discord.ext import commands

import tagged
from logger import Logger


class Base(commands.Cog, tagged.Tagged):
    def __init__(self, bot):
        self.bot = bot
        self.TAG = type(self).__name__

    @commands.Cog.listener()
    async def on_ready(self):
        Logger.i(self, "bot ready as {0.user}".format(self.bot))
        Logger.divider()
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("with Kappa"))

    async def cog_command_error(self, ctx, error):
        Logger.e(self, f"{error}")


def setup(bot):
    bot.add_cog(Base(bot))
