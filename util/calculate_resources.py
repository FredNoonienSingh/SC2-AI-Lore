'''python'''
from typing import Union

'''sc2'''
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.game_data import Cost 
from sc2.ids.unit_typeid import UnitTypeId

'''util'''
from util.in_proximity import structure_in_proximity


class CalculationsResources:

    def __init__(self, bot:BotAI) -> None:
        self.bot = bot

    def calculate_available_resources(self) -> list[int, int]:
        minerals:int = 0
        vespene:int = 0
        for expansion in self.bot.expansion_locations_dict:
            minerals += sum([structure.mineral_contents if structure.is_mineral_field else 0 for structure in self.bot.expansion_locations_dict.get(expansion)])
            vespene += sum([structure.vespene_contents if structure.is_vespene_geyser else 0 for structure in self.bot.expansion_locations_dict.get(expansion)])
        return (minerals, vespene)

    def calculate_tapped_resources(self) -> int:
        minerals: int = 0
        vespene: int = 0
        # stupid because it does not account for ownership of structures / also slow / pure idiocy 
        for expansion in self.bot.expansion_locations:
            if structure_in_proximity(self.bot,UnitTypeId.NEXUS,expansion,10):
               minerals += sum([structure.mineral_contents if structure.is_mineral_field else 0 for structure in self.bot.expansion_locations_dict.get(expansion)])
            if structure_in_proximity(self.bot,UnitTypeId.ASSIMILATOR,expansion,3):
                vespene += sum([structure.vespene_contents if structure.is_vespene_geyser else 0 for structure in self.bot.expansion_locations_dict.get(expansion)]) 
        return (minerals, vespene)

    def calculate_destroyed_resources(self) -> int:
        #for enemy in self.bot.enemy
        pass

    def calculate_lost_resources(self) -> int:
        pass
    
    def estimate_enemy_income(self):
        # View Repo SC2-Replay-Data Analysis for more details how this is working 
        pass

    def estimate_economy_damage(self):
        """returns tuple(int,int, float) lost minerals, gas, percentage economy destroyed/lost"""
        pass

