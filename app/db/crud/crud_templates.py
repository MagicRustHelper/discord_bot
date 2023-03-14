from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import MessageTemplateModel
from app.tools.template import MessageTemplates


class CRUDTemplates:
    def __init__(self) -> None:
        self.model = MessageTemplateModel

    async def get_template(self, session: AsyncSession, *, name: str) -> MessageTemplateModel:
        statement = select(self.model).where(self.model.name == name)
        template_obj = await session.scalar(statement)
        return template_obj

    async def create_template(self, session: AsyncSession, *, msg_template: MessageTemplates) -> None:
        obj_in = self.model(
            name=msg_template.name,
            text=msg_template.text,
            image_url=msg_template.image_url,
        )
        session.add(obj_in)
        await session.commit()

    async def get_all_names(self, session: AsyncSession) -> list[str]:
        statement = select(self.model.name)
        template_objs = await session.scalars(statement)
        return template_objs.all()

    async def delete_template(self, session: AsyncSession, *, name: str) -> None:
        statement = delete(self.model).where(self.model.name == name)
        await session.execute(statement)
        await session.commit()

    async def edit_template(self, session: AsyncSession, *, old_name: str, new_msg_template: MessageTemplates) -> None:
        template_obj = await self.get_template(session, name=old_name)
        template_obj.name = new_msg_template.name
        template_obj.text = new_msg_template.text
        template_obj.image_url = new_msg_template.image_url
        session.add(template_obj)
        await session.commit()


templates = CRUDTemplates()
