from typing import TYPE_CHECKING

import discord

from app.tools import find_friend_cooldown

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriendModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title='Поиск друга!')

        self.add_item(
            discord.ui.InputText(
                label='Заголовок', placeholder='Ищу команду, напарника. Проводим набор в клан', max_length=50
            )
        )
        self.add_item(
            discord.ui.InputText(
                label='Текст',
                style=discord.InputTextStyle.long,
                required=False,
                placeholder='Мне 19 лет, адекват, 500 часов.\nили\nФорма заявки: ...',
            )
        )
        self.add_item(
            discord.ui.InputText(
                label='Номер(а) сервера(-ов)',
                placeholder='1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18',
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        client: 'MRHelperBot' = interaction.client
        find_friend_cooldown.add_cooldown(user_id=interaction.user.id, cooldown=client.settings.find_friends_cooldown)

        embed = discord.Embed(
            title=self.children[0].value, color=discord.Color.blurple()
        )  # TODO: Поставить цвет приблежнный к магик расту

        embed.set_author(
            name=interaction.user.name,
            icon_url=self._get_avatar(interaction, client),
        )
        embed.add_field(name='', value=self.children[1].value, inline=False)
        embed.add_field(name='Сервера', value=self.children[2].value, inline=False)
        embed.add_field(name='', value=interaction.user.mention)

        find_friend_channel = await interaction.guild.fetch_channel(client.settings.find_friends_channel)
        await find_friend_channel.send(embed=embed)
        await interaction.response.send_message('Форма отправлена.', ephemeral=True)
        # await interaction.response.send_message(embeds=[embed])

    def _get_avatar(self, interaction: discord.Interaction, client: 'MRHelperBot') -> str:
        if interaction.user.avatar:
            return interaction.user.avatar.url
        else:
            return client.settings.magic_avatar_url
