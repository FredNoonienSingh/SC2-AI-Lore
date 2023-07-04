
"""python modules"""
from random import choice

"""sc2"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human

"""build_orders"""
from builds.fast_blink import FAST_BLINK

"""abstractions"""
from micro import micro
from macro import macro

"""Utils"""
from util.camera import camera

"""Banter"""
from banter.banter import greeting

"""Constants"""
from constants.map_list import MAP_LIST

from debugTools.unit_vision import render_unit_vision
from debugTools.unit_lable import unit_label
from debugTools.gameinfo import draw_gameinfo
from debugTools.unit_range import unit_range

class B4(BotAI):

    def __init__(self, debug:bool=False)->None:
        self.race = Race.Protoss
        self.name = "B-4"
        self.version = "0.1"
        self.army_groups = []
        self.debug = debug

    async def on_start(self):
        #print(FAST_BLINK)
        await greeting(self)
        expand_locs = list(self.expansion_locations)
        for expansion in list(expand_locs):
            self.workers.prefer_idle.closest_to(expansion).move(expansion, True)

    async def on_step(self, iteration:int):

            if self.townhalls and self.units:
                await macro(self)
                await micro(self)
                if self.debug:
                    draw_gameinfo(self)
                    await camera(self)
                    for unit in self.enemy_units:
                        self.client.debug_sphere_out(unit, unit.ground_range, (255,255,0))
                        self.client.debug_sphere_out(unit, unit.air_range, (255,255,0))
                    for unit in self.units:
                        unit_label(self, unit)
                        unit_range(self, unit)
                        render_unit_vision(self, unit)
                return 
            await self.client.leave()

if __name__ == "__main__":
    AiPlayer = B4()
    run_game(maps.get(choice(MAP_LIST)), 
             [
                Bot(AiPlayer.race, B4(debug=False)),
                Computer(choice([Race.Terran,Race.Zerg,Race.Protoss]), Difficulty.Hard)
            ], 
        realtime=True
        )
