from typing import TYPE_CHECKING, Optional

import discord
from loguru import logger

from app.core import utils

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class SendMessage(discord.ui.Modal):
    def __init__(self, client: 'MRHelperBot', template: Optional[str] = None) -> None:
        self.client = client
        self.template = template

        title = 'Отправка сообщения от бота'
        title += f'с шаблоном {template}' if template else ''
        if len(title) > 45:
            title = title[:45]
        super().__init__(title=title)

        self.add_item(
            discord.ui.InputText(
                label='Текст',
                placeholder='Вышло обновление и давали писи с попами!! И в расте можно какать.',
                style=discord.InputTextStyle.long,
                required=False,
            ),
        )

        self.add_item(
            discord.ui.InputText(
                label='Ссылка на картинку',
                placeholder='Прямая ссылка на картинку',
                required=False,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            color=utils.get_random_blue_color(),
        )
        embed.set_author(
            name='MagicRust',
            icon_url=self.client.settings.magic_avatar_url,
            url=self.client.settings.VK_MAGIC_RUST_URL,
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
        message = await channel.send(embed=embed)
        logger.info(f'{interaction.user} опубликовал новость от имени бота в канал {channel} ID: {message.id}')
        await interaction.response.send_message('Новость отправлена!', ephemeral=True)
