from typing import TYPE_CHECKING

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from app.core import messages, utils
from app.modals import SendMessage

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class BotMessage(commands.Cog):
    def __init__(self, bot: 'MRHelperBot') -> None:
        self.bot = bot

    msg = SlashCommandGroup(
        'msg',
        description='Сообщения от бота',
        default_member_permissions=discord.Permissions(administrator=True),
        checks=[utils.is_ctx_from_admin],
    )

    @msg.command(description='Отправка сообщения от имени бота в текущий канал')
    async def send(self, ctx: discord.ApplicationContext, template: discord.Option(str, required=False)) -> None:
        await ctx.send_modal(SendMessage(self.bot, template))

    @msg.error
    async def msg_on_error(self, ctx: discord.ApplicationContext, error: commands.CommandError) -> None:  # noqa: ARG002
        await ctx.interaction.response.send_message(messages.SOMETHING_WRONG, ephemeral=True)


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(BotMessage(bot))
