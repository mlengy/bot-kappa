from dotenv import dotenv_values
from discord.ext import commands

PREFIX = '`'
bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    print('on_ready as {0.user}'.format(bot))


@bot.command(
    help="uwu?",
    brief="uwu?"
)
async def hi(ctx):
    await ctx.channel.send("uwu")


token = dotenv_values(".env.token")["TOKEN"]
bot.run(token)
