from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import MRHelperBot


class GetLogs(commands.Cog):
    def __init__(self, bot: 'MRHelperBot') -> None:
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def get_info_logs(self, ctx: discord.ApplicationContext) -> None:
        await ctx.author.send(file=discord.File('logs/info.log', 'rb'))

    @commands.slash_command()
    @commands.is_owner()
    async def get_debug_logs(self, ctx: discord.ApplicationContext) -> None:
        await ctx.author.send(file=discord.File('logs/debug.log', 'rb'))


def setup(bot: 'MRHelperBot') -> None:
    bot.add_cog(GetLogs(bot))
