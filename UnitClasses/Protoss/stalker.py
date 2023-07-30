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
"""
Stalker Stats: 
    range: 6
    Blink Range: 7
"""

class Stalker(Unit):

    def __init__(self, 
                 proto_data, 
                 bot_object: BotAI, 
                 distance_calculation_index: int = -1, 
                 base_build: int = -1):
        super().__init__(proto_data, bot_object, distance_calculation_index, base_build)
        self.bot: BotAI = bot_object
        self.attack_state: bool = False
        self.target: Union[Point3, Unit] = self.calculate_target()
        self.vision = VisionLines(self.bot, self)
    
    async def blink(self, target:Union[Point3, Unit]):
        self.bot.do(self(AbilityId.EFFECT_BLINK_STALKER,target))
    
    async def offensive_blink(self, enemy:Unit):
        if len(self.bot.enemy_units.closer_than(9, enemy))<=len(self.bot.units(UnitTypeId.STALKER).closer_than(9,self)):
            await self.blink(self, enemy.position)

    async def defensive_blink(self,  enemy:Unit):
        position : Point3 = self.position.towards(enemy, -7)
        if not self.bot.enemy_units.closer_than(5, position):
            await blink(self,position)

    async def fight(self):
           if self.bot.enemy_units:
                enemy : Unit = self.target   # Filter for army units
        
                if self.distance_to(enemy)>self.ground_range:
                    self.move(enemy)        
                elif self.distance_to(enemy)<=self.ground_range:
                    self.attack(enemy)
        
                if not enemy.ground_range >= self.ground_range:
                    if enemy.distance_to(self) <= enemy.ground_range:
                        await kite(self.bot,self, enemy)
        
                distance : float = self.distance_to(enemy)
                if distance > 2 and distance < 15:
                    await self.offensive_blink(enemy)
    
                if self.shield_percentage < 0.25 and self.bot.enemy_units:
                    enemy : Unit = self.bot.enemy_units.closest_to(self)
                    await self.defensive_blink(self, enemy)
                    await stay_out_of_range(self.bot, self)

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