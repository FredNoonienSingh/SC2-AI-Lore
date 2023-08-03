from typing import Union

from numpy import sqrt
"""SC2"""
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI 
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.buff_id import BuffId
from sc2.data import Race
"""Actions"""
from actions.abilities import blink
from actions.stay_out_of_range import stay_out_of_range
from actions.kite import kite # kite_towards, kite_away

"""Utils"""
from util.in_proximity import unit_in_proximity
#from util.vision_lines import VisionLines
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
        self.attack_state: bool = True
        self.target: Unit = None
        self.way_point: Point3 = None
        #self.vision = VisionLines(self.bot, self)
    
    async def blink(self, target:Union[Point3, Unit]):
        self.bot.do(self(AbilityId.EFFECT_BLINK_STALKER,target))
    
    async def offensive_blink(self, enemy:Unit):
        if len(self.bot.enemy_units.closer_than(9, enemy))<=len(self.bot.units(UnitTypeId.STALKER).closer_than(9,self)):
            await self.blink(enemy.position)

    async def defensive_blink(self,  enemy:Unit):
        position : Point3 = self.position.towards(enemy, -7)
        if not self.bot.enemy_units.closer_than(5, position):
            await blink(position)

    async def fight(self):
            if isinstance(self.target,Unit):
                enemy = self.target
        
                if self.distance_to(enemy)>self.ground_range:
                    self.move(enemy)        
                elif self.distance_to(enemy)<=self.ground_range:
                    self.attack(enemy)

                for e in self.bot.enemy_units.closer_than(15, self):
                    if e.ground_range < self.ground_range:
                        if e.distance_to(self) < self.ground_range -1:
                            await kite(self.bot,self)
        
                distance : float = self.distance_to(enemy)
                if distance > 2 and distance < 15:
                    pass 
                    # await self.offensive_blink(enemy)
    
                if self.shield_percentage < 0.25 and self.bot.enemy_units:
                    enemy : Unit = self.bot.enemy_units.closest_to(self)
                    #
                    # await self.defensive_blink(enemy)
                    await stay_out_of_range(self.bot, self)
            else:
                self.attack(self.target)
   

    def calculate_target(self) -> None:
        HEALTH_WEIGHT, DPS_WEIGHT = 0.67, 0.33
        WORKERS = [UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE, UnitTypeId.MULE]
        IGNORED_UNITS: list = [UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.EGG]
        PREFERRED_UNITS: list = [UnitTypeId.GHOST, UnitTypeId.CARRIER, UnitTypeId.LURKER]
        enemy_units:Units = self.bot.enemy_units.filter(lambda unit: unit.type_id not in IGNORED_UNITS)
        
        if not enemy_units: 
            enemy_units: Units = self.bot.enemy_units
        
        close_allies:Units = self.bot.units.closest_n_units(self, 5)
        targeted_enemies: dict = {stalker.target:stalker for stalker in self.bot.stalkers}
        enemies_in_range: Units = enemy_units.closer_than(self.ground_range, self)
        enemies_in_sight: Units = enemy_units.closer_than(self.sight_range, self)

        enemy_dps_in_range = sum([unit.ground_dps for unit in enemies_in_range])
        enemy_health_in_range = sum([unit.health for unit in enemies_in_range])

        temp_target = []
        temp = 999
        for enemy in enemies_in_range: 
            if enemy.type_id in WORKERS:
                if not enemy.is_attacking and [unit for unit in enemies_in_sight if unit.type_id not in WORKERS]: 
                    if enemy in targeted_enemies.keys():
                        attacking_unit:Unit = targeted_enemies.get(enemy)
                        damage = attacking_unit.calculate_damage_vs_target(enemy)
                        if enemy.health - damage[0] > self.calculate_damage_vs_target(enemy)[0]*-1:
                            if not len(temp_target) or self.distance_to(enemy) < self.distance_to(temp_target[0]):
                                temp_target.insert(0, enemy)
                                continue
 
            dps_reduction = enemy_dps_in_range - enemy.ground_dps
            if enemy in targeted_enemies.keys():
                attacking_unit:Unit = targeted_enemies.get(enemy)
                damage = attacking_unit.calculate_damage_vs_target(enemy)
                if enemy.health - damage[0] > self.calculate_damage_vs_target(enemy)[0]*-1:
                    if not len(temp_target) or dps_reduction < enemy_dps_in_range - enemy.ground_dps:
                        temp_target.insert(0, enemy)
                        continue
            damage = self.calculate_damage_vs_target(enemy)[0]
            health_reduction = enemy_health_in_range - damage

            
            target_weight = sqrt(health_reduction**2*HEALTH_WEIGHT + dps_reduction**2*DPS_WEIGHT)
            if target_weight < temp:   
                temp_target.insert(0, enemy)
                temp = target_weight
                        

        if len(temp_target) > 0:
            self.target = temp_target[0]

    def calculate_path(self) -> None:
       self.way_point = self.bot.enemy_start_locations[0].towards(self, 3)
            

    async def update(self): 
        #self.vision.update()
        self.calculate_target()
        self.attack_state = True
        self.calculate_path()
        if self.weapon_ready:
            await self.fight()
            return 
        self.move(self.way_point) 


