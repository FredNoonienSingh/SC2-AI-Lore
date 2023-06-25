from sc2.unit import Unit
from sc2.bot_ai import BotAI 

from actions.abilities import prismaticaligment
from actions.stay_out_of_range import stay_out_of_range

async def voidray_micro(bot:BotAI, voidray:Unit, enemy_airforce:list, enemy_ground_units:list):
    
    if voidray.is_idle and enemy_airforce: 
        enemy = enemy_airforce.closest_to(voidray)
        if enemy.is_armored:
            await prismaticaligment(bot,voidray)
        voidray.attack(enemy)
    
    elif voidray.is_idle and enemy_ground_units:
        enemy = enemy_ground_units.closest_to(voidray)
        voidray.attack(enemy)
    
    else: 
        await stay_out_of_range(bot, voidray)