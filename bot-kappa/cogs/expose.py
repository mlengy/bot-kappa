from dotenv import dotenv_values
from discord.ext import commands

import constants
import tagged
from logger import Logger


class Expose(commands.Cog, tagged.Tagged):
    def __init__(self, bot):
        self.bot = bot
        self.TAG = type(self).__name__
        self.expose_mode_include = True

        expose_admin_strings = dotenv_values(constants.CONFIG_FILE)[constants.EXPOSE_ADMINS_KEY].split('\n')
        for admin in expose_admin_strings:
            Logger.v(self, f"Admin: {admin}")
        self.expose_admins = {
            int(admin[0]): admin[1] for admin in (admin.split(":") for admin in expose_admin_strings)
        }
        self.expose_subadmins = {}
        expose_exclude_strings = dotenv_values(constants.CONFIG_FILE)[constants.EXPOSE_EXCLUDE_KEY].split('\n')
        for exclude in expose_exclude_strings:
            Logger.v(self, f"Exclude: {exclude}")
        self.expose_exclude = {
            int(admin[0]): admin[1] for admin in (admin.split(":") for admin in expose_exclude_strings)
        }
        self.expose_include = {}

    @commands.command(
        help="replies with current expose mode",
        brief="replies with current expose mode"
    )
    async def expose_mode(self, ctx):
        mode = "include" if self.expose_mode_include else "exclude"
        await ctx.channel.send(f"Expose mode: {mode}")

    @commands.command(
        help="toggles current expose mode",
        brief="toggles current expose mode"
    )
    async def expose_mode_toggle(self, ctx):
        if await self.admin_guard(ctx):
            return

        self.expose_mode_include = not self.expose_mode_include

        mode = "include" if self.expose_mode_include else "exclude"
        await ctx.channel.send(f"New expose mode: {mode}")

    @commands.command(
        help="shows expose admins",
        brief="shows expose admins"
    )
    async def expose_admin(self, ctx):
        await self.print_group("Expose admins:", self.expose_admins | self.expose_subadmins, ctx)

    @commands.command(
        help="add an expose admin",
        brief="add an expose admin"
    )
    async def expose_add_admin(self, ctx):
        await self.add_to_group(self.expose_subadmins, ctx)

    @commands.command(
        help="remove an expose admin",
        brief="remove an expose admin"
    )
    async def expose_remove_admin(self, ctx):
        await self.remove_from_group(self.expose_subadmins, ctx)

    @commands.command(
        help="shows expose excludes",
        brief="shows expose excludes"
    )
    async def expose_exclude(self, ctx):
        await self.print_group("Expose excludes:", self.expose_exclude, ctx)

    @commands.command(
        help="add someone to the exclude list",
        brief="add someone to the exclude list"
    )
    async def expose_add_exclude(self, ctx):
        await self.add_to_group(self.expose_exclude, ctx)

    @commands.command(
        help="remove someone from the exclude list",
        brief="remove someone from the exclude list"
    )
    async def expose_remove_exclude(self, ctx):
        await self.remove_from_group(self.expose_exclude, ctx)

    @commands.command(
        help="shows expose includes",
        brief="shows expose includes"
    )
    async def expose_include(self, ctx):
        await self.print_group("Expose includes:", self.expose_include, ctx)

    @commands.command(
        help="add someone to the include list",
        brief="add someone to the include list"
    )
    async def expose_add_include(self, ctx):
        await self.add_to_group(self.expose_include, ctx)

    @commands.command(
        help="remove someone from the include list",
        brief="remove someone from the include list"
    )
    async def expose_remove_include(self, ctx):
        await self.remove_from_group(self.expose_include, ctx)

    async def add_to_group(self, group, ctx):
        if await self.admin_guard(ctx):
            return

        added = False

        mentioned_id = ctx.message.mentions[0].id
        mentioned_name = ctx.message.mentions[0].display_name
        if mentioned_id is not None and mentioned_id not in group:
            group[mentioned_id] = mentioned_name if mentioned_name else "Unknown"
            added = True

        if added:
            if mentioned_name is None:
                await ctx.channel.send("Added!")
            else:
                await ctx.channel.send(f"Added {mentioned_name}!")

    async def remove_from_group(self, group, ctx):
        if await self.admin_guard(ctx):
            return

        removed = False

        mentioned_id = ctx.message.mentions[0].id
        if mentioned_id is not None and mentioned_id in group:
            del group[mentioned_id]
            removed = True

        mentioned_name = ctx.message.mentions[0].display_name
        if removed:
            if mentioned_name is None:
                await ctx.channel.send("Removed!")
            else:
                await ctx.channel.send(f"Removed {mentioned_name}!")

    async def print_group(self, name, group, ctx):
        if await self.admin_guard(ctx):
            return

        group_string = '\n'.join(['`%s`: %s' % (key, value) for (key, value) in group.items()])

        await ctx.channel.send(f"{name}\n{group_string}")

    async def admin_guard(self, ctx):
        is_admin = ctx.author.id in self.expose_admins
        is_subadmin = ctx.author.id in self.expose_subadmins
        is_allowed = is_admin or is_subadmin

        if not is_allowed:
            await ctx.channel.send("Nice try.")

        return not is_allowed

    async def user_guard(self, userId):
        if self.expose_mode_include:
            if userId in self.expose_include:
                return False
            else:
                return True
        else:
            if userId in self.expose_exclude:
                return True
            else:
                return False

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        Logger.v(self, f"User [{message.author.display_name}] deleted a message!")
        Logger.v(self, f"Message: [{message.content}]")

        if await self.user_guard(message.author.id):
            return

        member_name = message.author.display_name
        member_pfp_url = message.author.display_avatar.url

        try:
            webhook = await message.channel.create_webhook(name=member_name)

            await webhook.send(message.content, username=member_name, avatar_url=member_pfp_url)
            await webhook.delete()
        except Exception as e:
            Logger.e(self, f"Failed to create webhook: {e}")

            await message.channel.send(f"{member_name} deleted: {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        Logger.v(self, f"User [{before.author.display_name}] edited a message!")
        Logger.v(self, f"Before: [{before.content}]")
        Logger.v(self, f"After: [{after.content}]")

        if await self.user_guard(before.author.id):
            return

        member_name = before.author.display_name
        member_pfp_url = before.author.display_avatar.url

        try:
            webhook = await before.channel.create_webhook(name=member_name)

            await webhook.send(before.content, username=member_name, avatar_url=member_pfp_url)
            await webhook.delete()
        except Exception as e:
            Logger.e(self, f"Failed to create webhook: {e}")

            await after.channel.send(f"{member_name} edited: {before.content}")


async def setup(bot):
    await bot.add_cog(Expose(bot))
