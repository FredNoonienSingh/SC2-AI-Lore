from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.ids.unit_typeid import UnitTypeId

from actions.abilities import blink
from actions.stay_out_of_range import stay_out_of_range

async def stalker_micro(bot:BotAI, stalker:Unit):
    if stalker.is_idle and bot.enemy_units:
        enemy = bot.enemy_units.closest_to(stalker)
        stalker.attack(enemy)
    if stalker.shield_percentage < 0.5 and bot.enemy_units :
            enemy = bot.enemy_units.closest_to(stalker)
            await stay_out_of_range(bot, stalker)