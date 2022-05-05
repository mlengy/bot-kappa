from dotenv import dotenv_values
from discord.ext import commands

import constants
import tagged
from logger import Logger
from base import Base


COG_TYPE_ESSENTIALS = "essentials"

ENABLED_COG_TYPES = {
    COG_TYPE_ESSENTIALS
}
COGS = {
    COG_TYPE_ESSENTIALS: [
        "utilities"
    ]
}


class Main(tagged.Tagged):
    def __init__(self):
        self.TAG = type(self).__name__

    @staticmethod
    def setup_cogs(bot):
        main = Main()
        Logger.i(main, "start cog setup")
        for cog_type in COGS:
            if cog_type in ENABLED_COG_TYPES:
                Logger.i(main, f"loading cogs in {cog_type}")
                for cog in COGS[cog_type]:
                    Logger.i(main, f"    loading cog {cog}")
                    bot.load_extension(f"cogs.{cog}")
            else:
                Logger.i(main, f"skipping cogs in {cog_type}")
        Logger.i(main, "finish cog setup")

    @staticmethod
    def main():
        if __name__ == "__main__":
            bot = commands.Bot(command_prefix=constants.PREFIX)

            bot.add_cog(Base(bot))
            Main.setup_cogs(bot)

            token = dotenv_values(constants.ENV_TOKEN)[constants.TOKEN_KEY]
            bot.run(token)


Main.main()
