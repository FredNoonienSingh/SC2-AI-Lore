from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId


async def build_gas(self : BotAI, nexus):
    vgs: Units = self.vespene_geyser.closer_than(12, nexus)
    for vg in vgs:
        if await self.can_place_single(UnitTypeId.REFINERY, vg.position):
            workers: Units = self.workers.gathering
            if workers:
                worker: Unit = workers.closest_to(vg)
                worker.build_gas(vg)