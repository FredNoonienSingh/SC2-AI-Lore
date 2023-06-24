from typing import Union
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

def in_target_area(bot:BotAI, unit, target:Union[Point2, Point3], area_radius:float) -> bool:
    unit_pos = unit.position
    print(unit_pos)