
from typing import Union

"""sc2"""
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId

"""utils"""
from util.can_build import can_build_unit

async def train_unit(bot:BotAI, unit: UnitTypeId, structure:UnitTypeId) -> bool:
    for structure in bot.structures(structure).idle:
        if can_build_unit(bot, unit):
            structure.train(unit)
            return True
        break
    return False 

async def warp_in_unit(bot: BotAI, unit:UnitTypeId, warp_in_position:Union[Point3, Unit]) -> bool:
    for gate in bot.structures(UnitTypeId.GATEWAY).idle:
        if can_build_unit(bot, unit):
            gate.warp_in(unit, warp_in_position)
            return True
        break
    return False