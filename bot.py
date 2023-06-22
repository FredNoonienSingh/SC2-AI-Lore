"""python modules"""

"""sc2"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


"""custom util"""
from util.in_proximity import structure_in_proximity
from util.can_build import can_build_unit, can_build_structure

class HalBot(BotAI):
    
    def __init__(self)->None:
        self.race = Race.Protoss
        self.name = "HalBot"
        self.version = "0.1"

    async def on_start(self):
        await self.chat_send(f"i am {self.name} Version {self.version}\n")

    async def on_step(self, iteration:int):
        if self.townhalls:
            await self.distribute_workers(resource_ratio=2)

            for nexus in self.structures(UnitTypeId.NEXUS):
                if nexus.surplus_harvesters < 0: 
                    if can_build_unit(self,UnitTypeId.PROBE) and not nexus.is_active:
                        nexus.train(UnitTypeId.PROBE)
                build_pos = nexus.position.towards(self.game_info.map_center)
                if not structure_in_proximity(self, "Pylon", nexus):
                    if can_build_structure(self,UnitTypeId.PYLON):
                        await self.build(UnitTypeId.PYLON, near=build_pos)
                if self.structures(UnitTypeId.FORGE) and not structure_in_proximity(self, "PhotonCannon", nexus):
                   if can_build_structure(self, UnitTypeId.PHOTONCANNON):
                        await self.build(UnitTypeId.PHOTONCANNON, near=build_pos)


            build_pos = self.main_base_ramp.protoss_wall_pylon.towards(self.game_info.map_center)

            if can_build_structure(self, UnitTypeId.GATEWAY):
                if len(self.structures(UnitTypeId.GATEWAY))<3: 
                    build_pos = self.main_base_ramp.protoss_wall_warpin.towards(self.game_info.map_center)
                    await self.build(UnitTypeId.GATEWAY, near=build_pos, build_worker=self.workers.prefer_idle.closest_to(build_pos))                
            
            if can_build_structure(self, UnitTypeId.FORGE) and self.structures(UnitTypeId.GATEWAY):
                if not self.structures(UnitTypeId.FORGE):
                    build_pos = self.main_base_ramp.protoss_wall_warpin.towards(self.game_info.map_center)
                    await self.build(UnitTypeId.FORGE, near=build_pos)
            
            if can_build_structure(self, UnitTypeId.PYLON) and self.supply_left<3 and not self.supply_cap == 200:
                await self.build(UnitTypeId.PYLON, near=build_pos, build_worker=self.workers.prefer_idle.closest_to(build_pos))
          
                    
            if not self.structures(UnitTypeId.CYBERNETICSCORE):
                if can_build_structure(self, UnitTypeId.CYBERNETICSCORE):
                    await self.build(UnitTypeId.CYBERNETICSCORE, near=build_pos)

            for gate in self.structures(UnitTypeId.GATEWAY):
                if can_build_unit(self, UnitTypeId.STALKER) and not gate.is_active:
                    gate.train(UnitTypeId.STALKER)
                if can_build_unit(self, UnitTypeId.ZEALOT) and not gate.is_active:
                    gate.train(UnitTypeId.ZEALOT)

            for zealot in self.units(UnitTypeId.ZEALOT):
                if zealot.is_idle:
                    zealot.move(self.game_info.map_center)
                #if len(self.units(UnitTypeId.ZEALOT))+len(self.units(UnitTypeId.STALKER))>100:
                 #   zealot.attack(self.enemy_start_locations[0])


            if can_build_structure(self,UnitTypeId.NEXUS):
                await self.expand_now()
        
        else: 
            await self.chat_send("gg (you are probably a smurfing hackcheater anyway !!!)")
            await self.client.leave()


if __name__ == "__main__":
    AiPlayer = HalBot()
    run_game(maps.get("BlackburnAIE"), [
        Bot(AiPlayer.race, HalBot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False)
