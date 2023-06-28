"""python modules"""

"""sc2"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human

"""abstractions"""
from micro import micro
from macro import macro

"""Utils"""
from util.camera import camera

"""Banter"""
#from banter.banter import greeting

class Lore(BotAI):

    def __init__(self, debug:bool=False)->None:
        self.race = Race.Protoss
        self.name = "HalBot"
        self.version = "0.1"
        self.army_groups = []
        self.debug = debug

    async def on_start(self):
        pass
        #await greeting(self)

    async def on_step(self, iteration:int):
            if self.townhalls and self.units:
                await macro(self)
                await micro(self)
                if self.debug:
                    for unit in self.enemy_units:
                        self.client.debug_sphere_out(unit, unit.ground_range, (255,255,0))
                        self.client.debug_sphere_out(unit, unit.air_range, (255,255,0))
                    for unit in self.units:
                        self.client.debug_sphere_out(unit, unit.ground_range, (0,255,0))
                        self.client.debug_sphere_out(unit, unit.air_range, (0,255,0))
                return 
            await self.client.leave()


if __name__ == "__main__":
    AiPlayer = Lore()
    
    run_game(maps.get("LightshadeAIE"), 
             [
                Bot(AiPlayer.race, AiPlayer(debug=True)),
                Computer(Race.Terran, Difficulty.Easy)
            ], 
        realtime=False
        )
