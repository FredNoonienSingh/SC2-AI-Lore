from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.position import Point3

from actions.stay_out_of_range import stay_out_of_range

async def kite(bot: BotAI,unit:Unit, enemy: Unit):
    position : Point3 = unit.position.towards(enemy, -2)
    
    if not unit.weapon_ready:
        await stay_out_of_range(bot, unit)
    elif unit.weapon_ready:
        unit.attack(enemy)