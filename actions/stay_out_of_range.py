
from sc2.bot_ai import BotAI
from sc2.unit import Unit

from util.in_proximity import unit_in_proximity

async def stay_out_of_range(bot:BotAI, unit:Unit):
    enemy_units = bot.enemy_units.closer_than(15, unit)
    # 15 is the hightest attack range in the Game / any unit further away cant be in range 
    for enemy in enemy_units:
        if not enemy.can_attack:
            continue
        if unit.is_flying:
            if enemy.can_attack_air and enemy.distance_to(unit)< enemy.air_range+.25:
                unit.move(unit.position.towards(enemy, -1))
                continue
        if enemy.can_attack_ground and enemy.distance_to(unit)<enemy.ground_range+.25:
            unit.move(unit.position.towards(enemy, -1))

    