from typing import TYPE_CHECKING

import discord

from app.core import app_config, utils
from app.tools import find_friend_cooldown

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriendModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title='Поиск друга!')

        self.add_item(
            discord.ui.InputText(
                label='Заголовок',
                placeholder='Ищу команду, напарника. Проводим набор в клан',
                max_length=50,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label='Текст',
                style=discord.InputTextStyle.long,
                required=False,
                placeholder='Мне 19 лет, адекват, 500 часов.\nили\nФорма заявки: ...',
                max_length=1024,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label='Номер(а) сервера(-ов) MAGIC RUST',
                placeholder='обязательно укажите НОМЕР(А) СЕРВЕРА(-ОВ) MR',
                max_length=20,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        client: 'MRHelperBot' = interaction.client
        if find_friend_cooldown.get_cooldown(interaction.user.id):
            return await interaction.response.send_message(
                'Хм... Либо ты пытался напокостить, либо что то пошло не так.', ephemeral=True
            )
        find_friend_cooldown.add_cooldown(user_id=interaction.user.id, cooldown=client.settings.find_friends_cooldown)

        embed = discord.Embed(title=self.children[0].value, color=utils.get_random_blue_color())

        embed.set_author(
            name=interaction.user.name,
            icon_url=self._get_avatar(interaction),
        )
        embed.add_field(name='', value=self.children[1].value, inline=False)
        server_text = self.children[2].value
        if not ('mr' in server_text.lower() or 'magic' in server_text.lower()):
            server_text = 'MR# ' + server_text
        embed.add_field(name='Сервер ', value=server_text, inline=False)

        find_friend_channel = await client.fetch_channel(client.settings.find_friends_channel)
        await find_friend_channel.send(content=interaction.user.mention, embed=embed)
        await interaction.response.send_message('Форма отправлена.', ephemeral=True)

    def _get_avatar(self, interaction: discord.Interaction) -> str:
        if interaction.user.avatar:
            return interaction.user.avatar.url
        else:
            return app_config.DEFAULT_DISCORD_AVATAR_LINK
