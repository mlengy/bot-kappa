from discord.ext import commands

import tagged
from logger import Logger


class Utilities(commands.Cog, tagged.Tagged):
    def __init__(self, bot):
        self.bot = bot
        self.TAG = type(self).__name__

    @commands.command(
        help="uwu?",
        brief="uwu?"
    )
    async def hi(self, ctx):
        Logger.v(self, f"got hi from {ctx.author}")
        await ctx.channel.send("uwu")

    async def cog_command_error(self, ctx, error):
        Logger.e(self, f"{error}")


async def setup(bot):
    await bot.add_cog(Utilities(bot))
