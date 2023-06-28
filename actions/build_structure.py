from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId


async def build_gas(self : BotAI, nexus):
    vespene: Units = self.vespene_geyser.closer_than(12, nexus)[0]
    if await self.can_place_single(UnitTypeId.REFINERY, vespene.position):
        workers: Units = self.workers.gathering
        if workers:
            worker: Unit = workers.closest_to(vespene)
            worker.build_gas(vespene)