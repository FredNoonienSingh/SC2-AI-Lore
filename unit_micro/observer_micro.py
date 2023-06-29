'''python'''
from random import randint

'''SC2'''
from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.position import Point3

"""utils"""
from util.postion_save import position_save

"""Actions"""
from actions.stay_out_of_range import stay_out_of_range


async def observer_micro(bot:BotAI, unit:Unit, target:Point3):
    if bot.enemy_units:
        enemy_center:Point3 = bot.enemy_units.center
        target = unit.position.towards(enemy_center, 2)
    else:
        target = unit.position.towards(bot.enemy_start_locations[0], 12) 
    if position_save(bot, target):
        unit.move(target) 
    await stay_out_of_range(bot, unit)