from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from app.core import messages
from app.modals import FindFriendModal
from app.tools import find_friend_cooldown

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriends(commands.Cog):
    def __init__(self, bot: 'MRHelperBot'):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def delete_message_in_friend_channel(self, message: discord.Message) -> None:
        if message.channel.id == self.bot.settings.find_friends_channel and not message.author.bot:
            await message.delete(reason='В канале разрешено только использования команды по поиску друга')
            await message.author.send(messages.MESSAGE_IN_FIND_CHANNEL)

    @commands.slash_command()
    @commands.dynamic_cooldown(find_friend_cooldown.discord_cooldown, type=commands.BucketType.user)
    async def friend(self, ctx: discord.ApplicationContext) -> None:
        await ctx.send_modal(FindFriendModal())

    @friend.error
    async def friend_on_error(self, ctx: discord.ApplicationContext, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            text = messages.FIND_COOLDOWN.format(error.cooldown.per, error.retry_after)
            await ctx.respond(text, ephemeral=True)


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(FindFriends(bot))
