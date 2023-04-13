from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from loguru import logger

from app.core import messages, utils
from app.modals import FindFriendModal
from app.tools import find_friend_cooldown
from app.tools.time import human_time

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriends(commands.Cog):
    def __init__(self, bot: 'MRHelperBot'):
        self.bot = bot

    @commands.slash_command(description='Создание формы на поиск друга')
    @commands.dynamic_cooldown(find_friend_cooldown.discord_cooldown, type=commands.BucketType.user)
    async def friend(self, ctx: discord.ApplicationContext) -> None:
        await ctx.send_modal(FindFriendModal())

    @commands.slash_command(
        checks=[utils.is_ctx_from_admin], default_member_permissions=discord.Permissions(administrator=True)
    )
    async def reset_cooldowns(self, ctx: discord.ApplicationContext, user: discord.Member) -> None:
        user_cooldown = self.friend._buckets._cache.get(user.id)
        if not user_cooldown:
            return await ctx.respond(
                f'У {user} нету кулдауна. Кулдаун фактически дается только после использования команды /friend в течение 24 часов. До этого он теоритический)))'
            )
        user_cooldown.reset()
        logger.info(f'{ctx.author} reset coldown to {user}:{user.id}')
        await ctx.respond('Кулдаун сброшен', ephemeral=True)

    @friend.error
    async def friend_on_error(self, ctx: discord.ApplicationContext, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            text = messages.FIND_COOLDOWN.format(
                human_time(self.bot.settings.find_friends_cooldown), human_time(error.retry_after)
            )
            await ctx.respond(text, ephemeral=True)


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(FindFriends(bot))
