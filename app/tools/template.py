from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from loguru import logger

from app.db import crud
from app.db.session import get_session

if TYPE_CHECKING:
    import discord


class MessageTemplates:
    def __init__(self, name: str, text: str | None = None, image_url: str | None = None) -> None:
        self.name = name
        self.text = text
        self.image_url = image_url

    async def add_template(self) -> None:
        async with get_session() as session:
            await crud.templates.create_template(session, msg_template=self)
            logger.info(f'Добавлен новый шаблон: {self}')

    async def update_template(self, new_template: MessageTemplates) -> None:
        async with get_session() as session:
            await crud.templates.edit_template(session, old_name=self.name, new_msg_template=new_template)
            logger.info(f'Шаблон {self.name} изменен было: \n{self}\nСтало:\n{new_template} ')

    @classmethod
    async def remove_template(cls: type[MessageTemplates], name: str) -> None:
        async with get_session() as session:
            await crud.templates.delete_template(session, name=name)

    @classmethod
    async def get_template(cls: type[MessageTemplates], name: str) -> MessageTemplates:
        async with get_session() as session:
            template = await crud.templates.get_template(session, name=name)

        template = asdict(template)
        del template['id']
        return cls(**template)

    @classmethod
    async def get_all_names(cls: type[MessageTemplates], *args, **kwargs) -> list[str]:  # noqa
        async with get_session() as session:
            return await crud.templates.get_all_names(session)

    @classmethod
    async def get_all_names_autocomplete(
        cls: type[MessageTemplates],
        msg_template: MessageTemplates,  # noqa: ARG003
        complete_ctx: 'discord.AutocompleteContext',
    ) -> list[str]:
        logger.debug(f'{complete_ctx.interaction.user} called template autocomplete')
        return await cls.get_all_names()

    def __repr__(self) -> str:
        return f'Название шаблона: {self.name}.\nТекст: {self.text}. Картинка: {self.image_url}'
