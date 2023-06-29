
"""SC2"""
from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId

"""Actions"""
from actions.kite import kite
from actions.abilities import blink
from actions.stay_out_of_range import stay_out_of_range

"""Utils"""
from util.in_proximity import unit_in_proximity

"""
Stalker Stats: 
    range: 6
    Blink Range: 7
"""

async def stalker_micro(bot:BotAI, stalker:Unit):
    
    if bot.enemy_units:
        enemy : Unit = bot.enemy_units.closest_to(stalker)    # Filter for army units
        if stalker.distance_to(enemy)>stalker.ground_range:
            stalker.move(enemy)
        
        elif stalker.distance_to(enemy)<=stalker.ground_range:
            stalker.attack(enemy)
        
        if not enemy.ground_range >= stalker.ground_range:
            if enemy.distance_to(stalker) <= enemy.ground_range:
                await kite(bot,stalker, enemy)
        
        distance : float = stalker.distance_to(enemy)
        if distance > 2 and distance < 15:
             await offensive_blink(bot, stalker, enemy)
    
    if stalker.shield_percentage < 0.25 and bot.enemy_units:
            enemy : Unit = bot.enemy_units.closest_to(stalker)
            await defensive_blink(bot, stalker, enemy)
            await stay_out_of_range(bot, stalker)

async def offensive_blink(bot:BotAI, stalker:Unit, enemy:Unit):
    if len(bot.enemy_units.closer_than(9, enemy))<=len(bot.units(UnitTypeId.STALKER).closer_than(9,stalker)):
        await blink(bot, stalker, enemy.position)

async def defensive_blink(bot:BotAI, stalker:Unit, enemy:Unit):
    position : Point3 = stalker.position.towards(enemy, -7)
    if not bot.enemy_units.closer_than(5, position):
        await blink(bot, stalker,position)