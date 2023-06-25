from sc2.unit import Unit
from sc2.bot_ai import BotAI 
from sc2.ids.unit_typeid import UnitTypeId

from actions.abilities import gravitonbeam
from actions.stay_out_of_range import stay_out_of_range

async def phoenix_micro(
        bot:BotAI,
        phoenix:Unit,
        enemy_airforce:list,
        enemy_ground_units:list
        ):
    
    PREFERRED_TARGETS:list = [UnitTypeId.SIEGETANK, UnitTypeId.SIEGETANKSIEGED,  UnitTypeId.LURKER]
    if phoenix.is_idle and enemy_airforce: 
        enemy = enemy_airforce.closest_to(phoenix)
        phoenix.attack(enemy)
    elif phoenix.energy >= 50 and enemy_ground_units:
        preferred_t = bot.enemy_units.filter(lambda unit: unit in PREFERRED_TARGETS and unit.closer_than(5, phoenix))
        if preferred_t:
            target = preferred_t.closest_to(phoenix)
        else:
            target = enemy_ground_units.closest_to(phoenix)
        await gravitonbeam(bot, phoenix,target)
    else:
        await stay_out_of_range(bot, phoenix)