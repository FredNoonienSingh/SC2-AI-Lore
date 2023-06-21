from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

class HalBot(BotAI):
    
    def __init__(self)->None:
        self.race = Race.Protoss
        self.name = "HalBot"
        self.version = "0.1"

    async def on_start(self):
        await self.chat_send(f"i am {self.name} v{self.version}")

    async def on_step(self, iteration:int):
        if self.townhalls: 
            if not self.structures(UnitTypeId.PYLON):
                build_pos = self.main_base_ramp.protoss_wall_pylon.towards(self.game_info.map_center)
                if self.can_afford(UnitTypeId.PYLON) and not self.already_pending(UnitTypeId.PYLON):
                    await self.build(UnitTypeId.PYLON, near=build_pos, build_worker=self.workers.prefer_idle.closest_to(build_pos))

        if not self.townhalls and not self.already_pending(UnitTypeId.NEXUS): 
            await self.chat_send("gg (you are probably a smurfing hackcheater anyway !!!)")
            await self.leave()





if __name__ == "__main__":
    AiPlayer = HalBot()
    run_game(maps.get("BlackburnAIE"), [
        Bot(AiPlayer.race, HalBot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False)
