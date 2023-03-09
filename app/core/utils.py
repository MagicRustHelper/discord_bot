import random
from typing import TYPE_CHECKING

from discord import ApplicationContext, Color
from loguru import logger

if TYPE_CHECKING:
    from app.bot import MRHelperBot


def get_random_blue_color() -> Color:
    blue_colors = (
        Color.blue,
        Color.blurple,
        Color.og_blurple,
        Color.og_blurple,
    )
    random_color_func = random.choice(blue_colors)
    return random_color_func()


async def is_ctx_from_admin(ctx: ApplicationContext) -> bool:
    bot: 'MRHelperBot' = ctx.bot
    bot_guilds = bot.guilds
    logger.debug('Bot guilds: {}', bot_guilds)

    # Получаем всех админов TODO: Вынести в другую функцию
    admins_id = set()
    for guild in bot_guilds:
        admin_roles = [role for role in guild.roles if role.permissions.administrator]
        admins_id.add(guild.owner_id)
        for role in admin_roles:
            for member in role.members:
                admins_id.add(member.id)

    if ctx.author.id in admins_id:
        return True
    return False
