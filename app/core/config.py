from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ApplicationConfig:
    intents: dict[str, bool] = {
        'members': True,
        'messages': True,
        'message_content': True,
        'guilds': True,
    }
    SQLALCHEMY_DATABASE_URI: str | None = None

    def __init__(self) -> None:
        self.SQLALCHEMY_DATABASE_URI = self.get_uri_from_env()

    def get_uri_from_env(self) -> str:
        user = os.getenv('POSTGRES_USER', 'postgres')
        password = os.getenv('POSTGRES_PASSWORD', 'postgres')
        server = os.getenv('POSTGRES_HOST', 'localhost')
        db = os.getenv('POSTGRES_DB', 'postgres')
        return f'postgresql+asyncpg://{user}:{password}@{server}/{db}'


app_config = ApplicationConfig()
