from typing import TYPE_CHECKING, Optional

import discord
from loguru import logger

from app.core import utils
from app.tools.template import MessageTemplates

if TYPE_CHECKING:
    from app.bot import MRHelperBot

MODAL_TITLE_MAX_LENGTH = 45


class SendMessageModal(discord.ui.Modal):
    def __init__(
        self, client: 'MRHelperBot', text: Optional[str] = None, template: Optional[MessageTemplates] = None
    ) -> None:
        self.text = text or ''
        self.client = client
        self.template = template

        title = 'Отправка сообщения от бота'
        title += f' с шаблоном {template.name}' if template else ''
        if len(title) > MODAL_TITLE_MAX_LENGTH:
            title = title[:MODAL_TITLE_MAX_LENGTH]
        super().__init__(title=title)

        if template:
            value_text, value_image = template.text, template.image_url
        else:
            value_text, value_image = None, None

        self.add_item(
            discord.ui.InputText(
                label='Текст',
                placeholder='Вышло обновление и давали писи с попами!! И в расте можно какать.',
                value=value_text,
                style=discord.InputTextStyle.long,
                required=False,
                max_length=1024,
            ),
        )

        self.add_item(
            discord.ui.InputText(
                label='Ссылка на картинку',
                placeholder='Прямая ссылка на картинку',
                value=value_image,
                required=False,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            color=utils.get_random_blue_color(),
        )

        embed.add_field(
            name='',
            value=self.children[0].value,
            inline=False,
        )

        image_url: str | None = self.children[1].value
        if image_url:
            embed.set_image(url=image_url)

        channel = await self.client.fetch_channel(interaction.channel_id)
        message = await channel.send(content=self.text, embed=embed)
        logger.info(f'{interaction.user} опубликовал новость от имени бота в канал {channel} ID: {message.id}')
        await interaction.response.send_message('Новость отправлена!', ephemeral=True)
