from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.declarative import Base


class DiscordConfig(Base):
    __tablename__ = 'discord_config'

    id: Mapped[int] = mapped_column(primary_key=True, default=0)
    magic_avatar_url: Mapped[Optional[str]] = mapped_column(default=None)

    # Find friends settings
    find_friends_cooldown: Mapped[Optional[int]] = mapped_column(BigInteger, default=None)
    find_friends_channel: Mapped[Optional[int]] = mapped_column(BigInteger, default=None)

    # Send by bot settings
