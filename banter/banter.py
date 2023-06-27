
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

from sc.unit import Unit 
from sc.units import Units 


async def greeting(bot:BotAI): 
    await bot.chat_send(f"i am {bot.name} Version {bot.version}")

