from typing import Union

"""sc2"""
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId

"""utils"""
from util.can_build import can_build_structure

async def build_gas(self : BotAI, nexus) -> bool:
    vespene: Units = self.vespene_geyser.closer_than(12, nexus)[0]
    if await self.can_place_single(UnitTypeId.REFINERY, vespene.position):
        workers: Units = self.workers.gathering
        if workers:
            worker: Unit = workers.closest_to(vespene)
            worker.build_gas(vespene)
            return True
    return False

async def build_structure(bot:BotAI, structure:UnitTypeId, build_pos:Union[Point3, Unit], worker) -> bool:
    if can_build_structure(bot, structure):
        await bot.build(structure,near=build_pos,build_worker=worker)
        return True
    return False