from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.buff_id import BuffId

"""Actions"""
from actions.kite import kite

"""Utils"""
from util.in_proximity import unit_in_proximity


"""
    Buff Name: BuffId.IMMORTALOVERLOAD
"""

async def immortal_micro(bot:BotAI, unit:Unit):
    BARRIER = BuffId.IMMORTALOVERLOAD
    units = bot.enemy_units.filter(lambda unit: unit.is_flying == False)
    if unit.is_idle and units:
        enemy : Unit = units.closest_to(unit)
        if bot.debug: 
                bot.client.debug_line_out(unit ,enemy, (255,0,0))
        unit.attack(enemy)
        if BARRIER in unit.buffs:
            unit.hold_position()
          
        else:
            await kite(bot, unit, enemy)