
"""python modules"""
import sqlite3
from random import choice


"""sc2"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

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

    def __init__(self, debug:bool=False)->None:
        self.race = Race.Protoss
        self.name = "B-4"
        self.version = "0.1"
        self.step = 0
        self.debug = debug
        self.build_order = None

    def choose_build_order(self) -> list:
        return FAST_BLINK

    async def on_start(self):
        self.build_order = self.choose_build_order()
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
        await super().on_unit_created(unit)       # Figure out why the API has a type assertion 
    
    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        return await super().on_unit_took_damage(unit, amount_damage_taken)
    
    async def on_unit_destroyed(self, unit_tag: int):
        return await super().on_unit_destroyed(unit_tag)
    
    async def on_building_construction_started(self, unit: Unit):
        return await super().on_building_construction_started(unit)
    
    async def on_building_construction_complete(self, unit: Unit):
        return await super().on_building_construction_complete(unit)
    
    async def on_enemy_unit_entered_vision(self, unit: Unit):
        return await super().on_enemy_unit_entered_vision(unit)
    
    async def on_enemy_unit_left_vision(self, unit_tag: int):
        return await super().on_enemy_unit_left_vision(unit_tag)
    
    async def on_upgrade_complete(self, upgrade: UpgradeId):
        return await super().on_upgrade_complete(upgrade)
    
    async def on_unit_type_changed(self, unit: Unit, previous_type: UnitTypeId):
        return await super().on_unit_type_changed(unit, previous_type)

if __name__ == "__main__":
    AiPlayer = B4()
    run_game(maps.get(choice(MAP_LIST)), 
             [
                Bot(AiPlayer.race, B4(debug=True)),
                Computer(choice([Race.Terran,Race.Zerg,Race.Protoss]),Difficulty.Hard)
            ], 
        realtime=True
        )
