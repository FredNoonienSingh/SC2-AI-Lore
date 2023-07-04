from typing import Union
from random import randint

from numpy import linspace
from math import sin, pi, cos, radians

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId


def render_unit_vision(bot: BotAI, unit:Unit):
    terrain_height = bot.get_terrain_z_height(unit)
    origin = Point3((unit.position.x, unit.position.y, terrain_height))
    space = [0, .25*pi, .5*pi, .75*pi, pi, 1.25*pi, 1.5*pi, 1.75*pi, 2*pi]
    vision_lines = [point_on_circle(bot,origin, deg) for deg in space]
    for line in vision_lines:
        color = (255, 255, 255)
        if bot.game_info.pathing_grid.is_set(line):
            color = (0, 0, 255)
        bot.client.debug_line_out(origin, line, color)


def point_on_circle(bot: BotAI, origin:Union[Unit, Point3],degree:float, radius:float=5) -> Point3:
    x,y= origin.x, origin.y
    x = int(x+(radius*cos(degree)))
    y = int(y+(radius+sin(degree)))

    terrain_height = bot.get_terrain_z_height(Point2((x,y)))
    return Point3((x,y,terrain_height))
