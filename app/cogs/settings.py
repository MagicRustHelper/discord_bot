from typing import TYPE_CHECKING

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from app.core import utils

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class Settings(commands.Cog):
    def __init__(self, bot: 'MRHelperBot'):
        self.bot = bot

    settings = SlashCommandGroup(
        'settings',
        description='Настройки бота',
        default_member_permissions=discord.Permissions(administrator=True),
        checks=[utils.is_ctx_from_admin],
    )

    @settings.command(description='Изменение кулдауна на поиск друга.')
    async def cooldown(self, ctx: discord.ApplicationContext, cooldown: discord.Option(int)) -> None:
        self.bot.settings.find_friends_cooldown = cooldown
        await ctx.respond(f'Кулдаун был обновлен до {cooldown} секунд.', ephemeral=True)

    @settings.command(description='Изменение канала, где искать друга.')
    async def friend_channel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel) -> None:
        self.bot.settings.find_friends_channel = channel.id
        await ctx.respond(f'Канал для поиска друга изменен на {channel}.', ephemeral=True)

    @settings.command(
        description='Аватарка магик раста, нужна для постов и используется как дефолтная если у человека нету.'
    )
    async def magic_avatar_url(self, ctx: discord.ApplicationContext, url: discord.Option(str)) -> None:
        self.bot.settings.magic_avatar_url = url
        await ctx.respond(f'Аватарка магик раста изменена на {url}.', ephemeral=True)

    @settings.command(description='Канал для отправки логов')
    async def log_channel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel) -> None:
        self.bot.settings.log_message_channel = channel.id
        await ctx.respond(f'Канал для логов изменена на {channel}', ephemeral=True)


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(Settings(bot))
