from datetime import datetime
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from app.core import messages, utils

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class FindFriendsEvents(commands.Cog):
    def __init__(self, bot: 'MRHelperBot'):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def delete_message_in_friend_channel(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if message.channel.id != self.bot.settings.find_friends_channel:
            return

        if message.guild.owner_id == message.author.id:
            return

        if utils.is_member_admin(message.author):
            return

        await message.delete(reason='В канале разрешено только использования команды по поиску друга')
        await message.author.send(messages.MESSAGE_IN_FIND_CHANNEL)

    @commands.Cog.listener('on_message_delete')
    async def log_deleted_message(self, message: discord.Message) -> None:
        if message.channel.id != self.bot.settings.find_friends_channel:
            return

        log_channel = await message.guild.fetch_channel(self.bot.settings.log_message_channel)
        if message.author.bot:
            text, message_member = await self._get_data_if_bot(message)
        else:
            return

        embed = self._build_log_embed(message, text, message_member)
        await log_channel.send(embed=embed)

    def _build_base_log_embed(self) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.nitro_pink(), timestamp=datetime.now())
        embed.add_field(name='', value='Сообщение было удалено', inline=False)
        return embed

    async def _get_data_if_bot(self, message: discord.Message) -> tuple[str, str]:
        text = self._parse_find_friend_embed(message.embeds[0])
        message_member = await message.guild.fetch_member(message.content[2:-1])
        return text, message_member

    def _build_log_embed(self, message: discord.Message, text: str, message_member: discord.Member) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.nitro_pink(), timestamp=datetime.now())
        embed.add_field(name='', value='Сообщение было удалено', inline=False)
        embed.add_field(name='Удалённое сообщение:', value=utils.framing_message(text), inline=False)
        embed.add_field(name='Автор', value=utils.bold_message(message_member.name) + f' ({message_member.mention})')
        embed.add_field(name='Канал', value=utils.bold_message(message.channel.name) + f' ({message.channel.mention})')
        embed.set_footer(text=f'Id сообщения: {message.id}')
        return embed

    def _parse_find_friend_embed(self, embed: discord.Embed) -> str:
        title = embed.title
        main_text = embed.fields[0].value
        server_field_name = embed.fields[1].name
        servers = embed.fields[1].value
        return f"""{title}

{main_text}

{server_field_name}
{servers}"""


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(FindFriendsEvents(bot))
