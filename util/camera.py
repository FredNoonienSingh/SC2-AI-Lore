
from sc2.bot_ai import BotAI 
from sc2.unit import Unit
from sc2.units import Units 
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId


async def camera(bot:BotAI):
        if bot.units(UnitTypeId.OBSERVER):
            stalker:Unit = bot.units(UnitTypeId.OBSERVER).closest_to(bot.enemy_start_locations[0])
            if stalker:
                await bot.client.move_camera(stalker)