from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="uwu?",
        brief="uwu?"
    )
    async def hi(self, ctx):
        await ctx.channel.send("uwu")
