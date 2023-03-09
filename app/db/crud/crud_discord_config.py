from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DiscordConfig


class CRUDDiscordConfig:
    def __init__(self) -> None:
        self.model = DiscordConfig

    async def create_if_not_exists(self, session: AsyncSession) -> None:
        if not (await session.get(self.model, 0)):
            logger.debug('Create row with dicord config')
            db_obj = self.model()
            session.add(db_obj)
            await session.commit()
        else:
            logger.debug('Row with discord config exist')

    async def get_config(self, session: AsyncSession) -> DiscordConfig:
        return await session.get(self.model, 0)

    async def update_config(self, session: AsyncSession, *, config: dict) -> DiscordConfig:
        config_obj = await self.get_config(session)
        for key, value in config.items():
            setattr(config_obj, key[1:], value)
        session.add(config_obj)
        await session.commit()
        await session.refresh(config_obj)
        return config_obj


discord_config = CRUDDiscordConfig()
