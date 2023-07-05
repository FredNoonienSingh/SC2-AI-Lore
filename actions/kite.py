from typing import Union

from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.position import Point3

from actions.stay_out_of_range import stay_out_of_range

async def kite(bot: BotAI,unit:Unit):
    position : Point3 = unit.position.towards(unit.target, -2)
    
    if unit.weapon_cooldown < 0:
        unit.move(position)
        #await stay_out_of_range(bot, unit)
    elif unit.weapon_cooldown == 0:
        unit.attack(unit.target)

async def kite_towards(bot:BotAI, unit:Unit, target_position:Union[Point3, Unit], kite_away:bool=False):
    increment:int = 1 if not kite_away else -1
    position: Point3 = unit.position.towards(target_position, increment)
    if unit.weapon_ready:
        unit.attack(unit.target)
    else: 
        unit.move(position)

