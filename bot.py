
"""python modules"""
from random import choice

"""sc2"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.unit import Unit
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

"""Debug Tools"""
from debugTools.unit_vision import render_unit_vision
from debugTools.unit_lable import unit_label
from debugTools.gameinfo import draw_gameinfo
from debugTools.unit_range import unit_range

#from UnitClasses.Protoss.probe import Probe
from util.calculate_resources import CalculationsResources
class B4(BotAI):

    def __init__(self, debug:bool=False, build_order:list=FAST_BLINK)->None:
        self.race = Race.Protoss
        self.name = "B-4"
        self.version = "0.1"
        self.step = 0
        self.debug = debug
        self.build_order = build_order 

    async def on_start(self):
        resource_calculator = CalculationsResources(self)
        print(resource_calculator.calculate_available_resources())
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
                    for unit in self.units:
                        unit_label(self, unit)
                        unit_range(self, unit)
                        render_unit_vision(self, unit)
                return 
            await self.client.leave()

    async def on_unit_created(self, unit: Unit):
        await super().on_unit_created(unit)

if __name__ == "__main__":
    AiPlayer = B4()
    run_game(maps.get(choice(MAP_LIST)), 
             [
                Bot(AiPlayer.race, B4(debug=True)),
                Computer(choice([Race.Terran,Race.Zerg,Race.Protoss]),Difficulty.Hard)
            ], 
        realtime=True
        )
