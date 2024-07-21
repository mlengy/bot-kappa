from discord.ext import commands

import tagged
from logger import Logger


class Expose(commands.Cog, tagged.Tagged):
    def __init__(self, bot):
        self.bot = bot
        self.TAG = type(self).__name__

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        Logger.v(self, f"Message was deleted!")
        member_name = message.author.display_name
        member_pfp_url = message.author.display_avatar.url

        webhook = await message.channel.create_webhook(name=member_name)

        await webhook.send(message.content, username=member_name, avatar_url=member_pfp_url)
        await webhook.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        Logger.v(self, f"Message was edited!")
        member_name = before.author.display_name
        member_pfp_url = before.author.display_avatar.url

        webhook = await before.channel.create_webhook(name=member_name)

        await webhook.send(before.content, username=member_name, avatar_url=member_pfp_url)
        await webhook.delete()


async def setup(bot):
    await bot.add_cog(Expose(bot))
