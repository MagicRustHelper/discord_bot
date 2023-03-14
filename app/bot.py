import os
from typing import NoReturn

import discord
from discord.ext import commands
from loguru import logger

from app.core import Settings, app_config

COGS = ('cogs.find_friends', 'cogs.find_friends_events', 'cogs.settings', 'cogs.bot_message', 'cogs.templates')


class MRHelperBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents(**app_config.intents), owner_id=app_config.OWNER_ID)

        self._find_friends_cooldowns = {}
        self.settings: Settings
        self.load_cogs()

    def load_cogs(self) -> None:
        for cog in COGS:
            cog_with_path = 'app.' + cog
            self.load_extension(cog_with_path)
            logger.debug(f'Cog {cog_with_path} is loaded')

    async def on_connect(self) -> None:
        self.settings = await Settings.load_from_db()
        logger.debug(f'Settings is loaded: {vars(self.settings)}')

        await self.sync_commands()

    async def on_ready(self) -> None:
        logger.info(f'{self.user} is ready!')

    def run(self) -> NoReturn:
        super().run(os.getenv('DISCORD_TOKEN'))
