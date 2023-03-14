from typing import TYPE_CHECKING

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from app.core import utils
from app.modals import CreateTemplateModal, EditTemplateModal
from app.tools.template import MessageTemplates

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class TemplateCog(commands.Cog):
    def __init__(self, bot: 'MRHelperBot') -> None:
        self.bot = bot

    templates = SlashCommandGroup(
        'templates',
        description='Управления шаблонами',
        default_member_permissions=discord.Permissions(administrator=True),
        checks=[utils.is_ctx_from_admin],
    )

    @templates.command(description='Создание нового шаблона')
    async def create(self, ctx: discord.ApplicationContext) -> None:
        await ctx.send_modal(CreateTemplateModal())

    @templates.command(description='Удаление шаблона сообщений')
    async def delete(
        self,
        ctx: discord.ApplicationContext,
        template_name: discord.Option(str, autocomplete=MessageTemplates.get_all_names_autocomplete),
    ) -> None:
        await MessageTemplates.remove_template(template_name)
        await ctx.respond(f'Шаблон {template_name} удален', ephemeral=True)

    @templates.command(description='Редактирование шаблонов')
    async def edit(
        self,
        ctx: discord.ApplicationContext,
        template_name: discord.Option(str, autocomplete=MessageTemplates.get_all_names_autocomplete),
    ) -> None:
        old_template = await MessageTemplates.get_template(template_name)
        await ctx.send_modal(EditTemplateModal(old_template))


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(TemplateCog(bot))
