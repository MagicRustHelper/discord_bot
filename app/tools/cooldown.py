import time
from typing import TYPE_CHECKING

from discord.ext.commands.cooldowns import Cooldown as PycordCooldown
from loguru import logger

if TYPE_CHECKING:
    import discord


class FindFriendsCooldown:
    def __init__(self) -> None:
        self._cooldowns = {}

    def add_cooldown(self, user_id: int, cooldown: float) -> None:
        """Added cooldown to find friend

        If already on cooldown nothing will happen
        """
        if not self._cooldowns.get(user_id):
            logger.debug(f'Add cooldown {user_id} expired after {cooldown}')
            self._cooldowns[user_id] = time.time() + cooldown

    def get_cooldown(self, user_id: int) -> int | None:
        """Return cooldown to find friends by user id

        If no cooldown return None
        """
        cooldown_expire_at = self._cooldowns.get(user_id)
        logger.debug(f'User {user_id} cooldown expired at = {cooldown_expire_at}. Now is {time.time()}')
        if cooldown_expire_at:
            if cooldown_expire_at >= time.time():
                return cooldown_expire_at - time.time()
            else:
                del self._cooldowns[user_id]
                return None
        else:
            return None

    def discord_cooldown(self, message: 'discord.Message') -> PycordCooldown | None:
        cooldown = self.get_cooldown(message.author.id)
        logger.debug(f'User {message.author.id} cooldown = {cooldown}')
        if cooldown:
            pycord_cooldown = PycordCooldown(rate=1, per=cooldown)
            pycord_cooldown.update_rate_limit()
            return pycord_cooldown
        else:
            return None


find_friend_cooldown = FindFriendsCooldown()
