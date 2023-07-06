from typing import Union,Tuple
from math import sin, pi, cos

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId

class VisionLines:

    def __init__(self,
                 bot: BotAI,  
                 unit:Unit, 
                 radius:int=8, 
                 count:int=16
                 ) -> None:

        self.bot = bot
        self.unit = unit
        self.radius = radius
        self.count = count
        self.__angle_increment = 2*pi/self.count
        self.lines = self.cast_lines()
    
    def cast_lines(self)-> list[tuple]:
        x,y = self.unit.position_tuple
        lines = []
        for i in range(self.count):
            angle = i*self.__angle_increment
            target_x = x + self.radius * cos(angle)
            target_y = y + self.radius * sin(angle)
            lines.append((target_x,target_y))
        return lines

    def check_endpoint(self)-> list[bool]:
        return [True if self.bot.game_info.pathing_grid.is_set(line) else False for line in self.lines]

    def propagate_lines(self):
        pass

    def update(self):
        self.cast_lines()
        self.check_endpoint()