from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.position import Point3

"""utils"""
from util.postion_save import position_save

"""Actions"""
from actions.stay_out_of_range import stay_out_of_range


async def observer_micro(bot:BotAI, unit:Unit, target:Point3):
    if bot.enemy_units:
        enemys_center:Point3 = bot.enemy_units.center
        target = unit.position.towards(enemys_center, 1)
        if position_save(bot, target):
            unit.move(target)
    await stay_out_of_range(bot, unit)