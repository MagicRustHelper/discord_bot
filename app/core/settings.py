from __future__ import annotations

import asyncio
from dataclasses import asdict

from loguru import logger

from app.db import crud
from app.db.session import get_session


class Settings:
    def __init__(
        self, find_friends_cooldown: int, find_friends_channel: int, magic_avatar_url: str, log_message_channel: int
    ) -> None:
        self._find_friends_cooldown: int = find_friends_cooldown
        self._find_friends_channel: int = find_friends_channel
        self._magic_avatar_url: str = magic_avatar_url
        self._log_message_channel: int = log_message_channel
        self.VK_MAGIC_RUST_URL: str = 'https://vk.com/magicowrust'
        self.loop = asyncio.get_event_loop()

    @property
    def find_friends_cooldown(self) -> int:
        return self._find_friends_cooldown

    @property
    def find_friends_channel(self) -> int:
        return self._find_friends_channel

    @property
    def magic_avatar_url(self) -> str:
        return self._magic_avatar_url

    @property
    def log_message_channel(self) -> str:
        return self._log_message_channel

    @find_friends_cooldown.setter
    def find_friends_cooldown(self, value: int) -> None:
        self._find_friends_cooldown = value
        self.loop.create_task(self.update_config_in_db())

    @find_friends_channel.setter
    def find_friends_channel(self, value: int) -> None:
        self._find_friends_channel = value
        self.loop.create_task(self.update_config_in_db())

    @magic_avatar_url.setter
    def magic_avatar_url(self, value: str) -> None:
        self._magic_avatar_url = value
        self.loop.create_task(self.update_config_in_db())

    @log_message_channel.setter
    def log_message_channel(self, value: int) -> None:
        self._log_message_channel = value
        self.loop.create_task(self.update_config_in_db())

    async def update_config_in_db(self) -> None:
        data = vars(self)
        logger.debug(f'Updating config in db: {data}')
        async with get_session() as session:
            await crud.discord_config.update_config(session, config=data)

    @classmethod
    async def load_from_db(cls: type[Settings]) -> Settings:
        async with get_session() as session:
            await crud.discord_config.create_if_not_exists(session)
            config = await crud.discord_config.get_config(session)
            config_dict = asdict(config)
            del config_dict['id']
            return cls(**config_dict)
