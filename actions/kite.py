from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.position import Point3

from actions.stay_out_of_range import stay_out_of_range

async def kite(bot: BotAI,unit:Unit, enemy: Unit):
    position : Point3 = unit.position.towards(enemy, -2)
    
    if unit.weapon_cooldown < 0:
        unit.move(position)
        if bot.debug:
            print(type(position))
            #bot.client.debug_line_out(unit, position, (0,200,0))
        #await stay_out_of_range(bot, unit)
    elif unit.weapon_cooldown == 0:
        unit.attack(enemy)
        if bot.debug:
            bot.client.debug_line_out(unit ,enemy, (255,0,0))