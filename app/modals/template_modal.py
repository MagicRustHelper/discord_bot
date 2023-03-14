from typing import TYPE_CHECKING

import discord
from loguru import logger

from app.tools.template import MessageTemplates

if TYPE_CHECKING:
    pass


class CreateTemplateModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title='Создание шаблона')
        self.add_item(
            discord.ui.InputText(
                label='Название шаблона',
                required=True,
                max_length=40,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label='Текст шаблона',
                required=False,
                style=discord.InputTextStyle.long,
                max_length=1024,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label='Прямая ссылка на картинку',
                required=False,
                max_length=500,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        new_template = MessageTemplates(
            name=self.children[0].value,
            text=self.children[1].value,
            image_url=self.children[2].value,
        )
        await new_template.add_template()
        logger.info(f'Создан новый шаблон {new_template.name} пользователем {interaction.user}({interaction.user.id})')
        await interaction.response.send_message(f'Шаблон {self.children[0].value} создан', ephemeral=True)


class EditTemplateModal(discord.ui.Modal):
    def __init__(self, old_template: MessageTemplates) -> None:
        self.old_template = old_template

        title = f'Редактирование шаблона {old_template.name}'
        super().__init__(title=title[:45])

        self.add_item(
            discord.ui.InputText(
                label='Название шаблона',
                value=old_template.name,
                required=True,
                max_length=40,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label='Текст шаблона',
                value=old_template.text,
                required=False,
                style=discord.InputTextStyle.long,
                max_length=1024,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label='Прямая ссылка на картинку',
                value=old_template.image_url,
                required=False,
                max_length=500,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        new_template = MessageTemplates(
            name=self.children[0].value,
            text=self.children[1].value,
            image_url=self.children[2].value,
        )
        await self.old_template.update_template(new_template)
        logger.info(f'Изменен шаблон {self.old_template.name} пользователем {interaction.user}({interaction.user.id})')
        await interaction.response.send_message(f'Шаблон {self.old_template.name} изменен', ephemeral=True)
