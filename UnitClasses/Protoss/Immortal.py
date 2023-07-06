from typing import Union

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


class Immortal(Unit):

    def __init__(self, proto_data, bot_object: BotAI, distance_calculation_index: int = -1, base_build: int = -1):
        super().__init__(proto_data, bot_object, distance_calculation_index, base_build)
        self.bot: BotAI = bot_object
        self.attack_state: bool = False
        self.target: Union[Point3, Unit] = self.calculate_target()
        self.vision = VisionLines(self.bot, self)
    
    async def fight(self):
        BARRIER = BuffId.IMMORTALOVERLOAD
        units = self.bot.enemy_units.filter(lambda unit: unit.is_flying == False)
        if self.is_idle and units:
            enemy : Unit = units.closest_to(self)
            if self.bot.debug: 
                    self.bot.client.debug_line_out(self ,self.target, (255,0,0))
            self.attack(enemy)
            if BARRIER in self.buffs:
                self.hold_position() 
            else:
                await kite(self.bot, self.unit, enemy)

    def calculate_target(self) -> Union[Point3, Unit]:
        pass

    def calculate_path(self) -> Union[Point3, Point2, Unit]:
        pass        
        # get ETA

        # check for obstacles and set position point accordingly

    async def update(self): 
        self.vision.update()
        self.calculate_target()
        self.calculate_path()
        
        if self.attack_state:
          self.fight()