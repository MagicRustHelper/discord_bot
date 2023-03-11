from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from app.core import messages, utils
from app.modals import FindFriendModal
from app.tools import find_friend_cooldown
from app.tools.time import human_time

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriends(commands.Cog):
    def __init__(self, bot: 'MRHelperBot'):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def delete_message_in_friend_channel(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if not (message.channel.id == self.bot.settings.find_friends_channel):
            return

        if message.guild.owner_id == message.author.id:
            return

        if utils.is_member_admin(message.author):
            return

        await message.delete(reason='В канале разрешено только использования команды по поиску друга')
        await message.author.send(messages.MESSAGE_IN_FIND_CHANNEL)

    @commands.slash_command()
    @commands.dynamic_cooldown(find_friend_cooldown.discord_cooldown, type=commands.BucketType.user)
    async def friend(self, ctx: discord.ApplicationContext) -> None:
        await ctx.send_modal(FindFriendModal())

    @friend.error
    async def friend_on_error(self, ctx: discord.ApplicationContext, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            text = messages.FIND_COOLDOWN.format(
                human_time(self.bot.settings.find_friends_cooldown), human_time(error.retry_after)
            )
            await ctx.respond(text, ephemeral=True)


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(FindFriends(bot))
