
from sc2.unit import Unit
from sc2.bot_ai import BotAI 

from actions.abilities import charge

async def zealot_micro(bot:BotAI, zealot:Unit, enemy_ground_units:list):
    if enemy_ground_units:
        enemy = enemy_ground_units.closest_n_units(zealot, 5)[0]
        if zealot.is_idle:
            zealot.attack(enemy)
            if zealot.distance_to(enemy)<=4:
                await charge(bot, zealot, enemy)