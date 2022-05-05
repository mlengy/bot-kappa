from dotenv import dotenv_values
from discord.ext import commands

import cogs.utilities

PREFIX = '`'
bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    print('on_ready as {0.user}'.format(bot))


if __name__ == "__main__":
    bot.add_cog(cogs.utilities.Utilities(bot))

    token = dotenv_values(".env.token")["TOKEN"]
    bot.run(token)
