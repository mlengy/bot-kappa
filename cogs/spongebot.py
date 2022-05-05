from discord.ext import commands
from enum import Enum
import random
import re

import constants
import tagged
from logger import Logger


AUTO_ENABLED = True
# amount of messages needed before next spongebot is between
# AUTO_MESSAGE_OFFSET and AUTO_MESSAGE_OFFSET + AUTO_MESSAGE_RANGE inclusive on both sides
AUTO_MESSAGE_OFFSET = 100
AUTO_MESSAGE_RANGE = 50

MODIFIER_STRINGS = [
    "*",
    "**",
    "***"
]


class Spongebot(commands.Cog, tagged.Tagged):
    def __init__(self, bot):
        self.bot = bot
        self.TAG = type(self).__name__
        self.message_counter = 0
        self.__compute_new_message_limit()

    @commands.command(
        help="turns your message into a mocking message",
        brief="turns your message into a mocking message"
    )
    async def mock(self, ctx):
        message = ctx.message
        text = message.clean_content[len(f"{constants.PREFIX}mock "):]
        modified_text = Spongebot.__spongebob_mock(self, text)

        if modified_text is None:
            return

        member_name = message.author.name
        member_pfp_url = message.author.avatar_url

        webhook = await ctx.channel.create_webhook(name=member_name)

        await message.delete()
        await webhook.send(modified_text, username=member_name, avatar_url=member_pfp_url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.message_counter < self.message_limit:
            self.message_counter += 1
            return
        else:
            self.message_counter = 0
            self.__compute_new_message_limit()

        if message.author == self.bot.user:
            return

        text = message.clean_content

        if text.startswith(constants.PREFIX):
            return

        modified_text = Spongebot.__spongebob_mock(self, text)

        if modified_text is not None:
            await message.reply(modified_text)

    @staticmethod
    def __spongebob_mock(spongebot, text):
        # remove custom emojis
        emoji_pattern = r'<:.*?:\d+?>'
        # remove existing modifiers, leading, and trailing whitespace
        clean_text = re.sub(emoji_pattern, '', text.replace('*', '')).strip()

        if len(clean_text) == 0:
            return None

        if clean_text.isspace():
            return None

        Logger.v(spongebot, f"spongebotting message: [\n{clean_text}\n]")

        # whether we are currently modifying characters, not modifying characters, or waiting for a gap
        modifier_status = Spongebot.ModifierStatus.NO_MODIFIER
        # previous modifier if we are currently modifying
        previous_modifier = Spongebot.Modifier.NONE
        # range in which to generate integers, including 0, excluding the value itself
        random_range = 6
        modified_text = ""

        for char in clean_text:
            modified_char = char

            # this random number determines if what case we use and what modification behavior is applied
            determiner = random.randrange(random_range)

            # use each case around half the time
            if determiner % 2 == 0:
                modified_char = modified_char.lower().swapcase()

            # start modification of characters if
            #     - we are not waiting for a gap or currently modifying
            #     - the next character is whitespace
            #     - our random determiner allows us to modify the characters
            if modifier_status == Spongebot.ModifierStatus.NO_MODIFIER and not char.isspace() and determiner < len(MODIFIER_STRINGS):
                # switch status to currently modifying
                modifier_status = Spongebot.ModifierStatus.YES_MODIFIER
                # store current modifier type
                previous_modifier = Spongebot.Modifier(determiner)
                # modify the character
                modified_char = f"{str(previous_modifier)}{modified_char}"
            # if we are currently modifying
            elif modifier_status == Spongebot.ModifierStatus.YES_MODIFIER:
                # finish modification of characters if
                #     - the next character is whitespace
                #     - our random determiner is different does not allow us to modify the characters
                #     - our determiner modifier type is different from our current modifier type
                if char.isspace() or determiner > len(MODIFIER_STRINGS) - 1 or previous_modifier != Spongebot.Modifier(determiner):
                    # switch status to skip next character for modification
                    modifier_status = Spongebot.ModifierStatus.GAP_MODIFIER
                    # cap off modification and append next character
                    modified_char = f"{str(previous_modifier)}{modified_char}"
                    # reset current modifier type
                    previous_modifier = Spongebot.Modifier.NONE
                # continue modification of characters
                else:
                    pass
            # if we are waiting for a gap
            else:
                # stop waiting for the gap
                modifier_status = Spongebot.ModifierStatus.NO_MODIFIER

            modified_text += modified_char

        # if modification hasn't finished but the string is over
        if modifier_status == Spongebot.ModifierStatus.YES_MODIFIER:
            # cap off the modification
            modified_text += str(previous_modifier)

        Logger.v(spongebot, f"spongebotted message: [\n{modified_text}\n]")
        return modified_text

    def __compute_new_message_limit(self):
        self.message_limit = random.randrange(AUTO_MESSAGE_RANGE + 1) + AUTO_MESSAGE_OFFSET

    async def cog_command_error(self, ctx, error):
        Logger.e(self, f"{error}")

    class Modifier(Enum):
        NONE = -1
        ITALIC = 0
        BOLD = 1
        ITALIC_BOLD = 2

        def __str__(self):
            if self == Spongebot.Modifier.NONE:
                return ""
            else:
                return MODIFIER_STRINGS[self.value]

    class ModifierStatus(Enum):
        NO_MODIFIER = 0
        GAP_MODIFIER = 1
        YES_MODIFIER = 2


def setup(bot):
    bot.add_cog(Spongebot(bot))
