from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.db.declarative import Base, intpk


class MessageTemplateModel(Base):
    __tablename__ = 'message_templates'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    text: Mapped[Optional[str]] = mapped_column(default=None)
    image_url: Mapped[Optional[str]] = mapped_column(default=None)
