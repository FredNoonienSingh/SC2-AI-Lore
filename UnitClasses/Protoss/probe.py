from typing import Union, enum 
from enum import Enum 
"""SC2"""
from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.buff_id import BuffId

"""Actions"""
from actions.abilities import blink
from actions.stay_out_of_range import stay_out_of_range
from actions.kite import kite, kite_towards, kite_away

"""Utils"""
from util.in_proximity import unit_in_proximity
from util.vision_lines import VisionLines

class Probe(Unit):
    def __init__(self, proto_data, bot_object: BotAI, distance_calculation_index: int = -1, base_build: int = -1):
        super().__init__(proto_data, bot_object, distance_calculation_index, base_build)
        self.bot: BotAI = bot_object
        self.attack_state: bool = False
        self.target: Union[Point3, Unit] = self.calculate_target()
        self.vision = VisionLines(self.bot, self)
        self.worker_type:WorkerType = WorkerType.MINER

        def calculate_target(self):
            pass 

        def calculate_path(self):
            pass

        def update(self):
            self.vision.update()
            self.calculate_target()
            self.calculate_path()
            if self.worker_type == WorkerType.MINER:
                pass
            elif self.worker_type == WorkerType.BUILDER:
                pass 
        

class WorkerType(Enum):
    MINER = 1
    BUILDER = 2
