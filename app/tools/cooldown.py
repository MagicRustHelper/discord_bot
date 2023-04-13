import time
from typing import TYPE_CHECKING

from discord.ext.commands.cooldowns import Cooldown as PycordCooldown
from loguru import logger

if TYPE_CHECKING:
    import discord


class FindFriendsCooldown:
    def __init__(self) -> None:
        self._cooldowns_expire = {}

    def add_cooldown(self, user_id: int, cooldown: float) -> None:
        """Added cooldown to find friend

        If already on cooldown nothing will happen
        """
        self._cooldowns_expire[user_id] = time.time() + cooldown
        logger.info(f'add cooldown expire for {user_id}. Expire at = {self._cooldowns_expire[user_id]}')

    def get_cooldown(self, user_id: int) -> int | None:
        """Return cooldown to find friends by user id

        If no cooldown return None
        """
        cooldown_expire_at = self._cooldowns_expire.get(user_id)
        logger.debug(f'User {user_id} cooldown expired at = {cooldown_expire_at}. Now is {time.time()}')
        if not cooldown_expire_at:
            return None
        if cooldown_expire_at >= time.time():
            return cooldown_expire_at - time.time()
        return None

    def discord_cooldown(self, message: 'discord.Message') -> PycordCooldown | None:
        cooldown = self.get_cooldown(message.author.id)
        logger.debug(f'User {message.author.id} cooldown = {cooldown}')
        if cooldown:
            del self._cooldowns_expire[message.author.id]
            logger.info(f'{message.author}:{message.author.id} now on cooldown at {cooldown}')
            pycord_cooldown = PycordCooldown(rate=1, per=cooldown)
            pycord_cooldown.update_rate_limit()
            return pycord_cooldown
        else:
            return None


find_friend_cooldown = FindFriendsCooldown()
