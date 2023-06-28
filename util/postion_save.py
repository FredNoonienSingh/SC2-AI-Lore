from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.units import Units

def position_save(bot:BotAI, position) -> bool:
    enemy_units:Units = bot.enemy_units.closer_than(15, position)
    # 15 is the hightest attack range in the Game / any unit further away cant be in range 
    enemy_structures:Units = bot.enemy_structures.closer_than(8, position)
    # 8 is the range of a turret with range upgrade - no structure has a higher range 
    possible_threads: list = [unit for unit in enemy_units]
    for structure in enemy_structures:
        possible_threads.append(structure)
    for enemy in possible_threads:
        if not enemy.can_attack:
            continue
        if enemy.can_attack_air and enemy.distance_to(position)< enemy.air_range+1:
            return False
        if enemy.can_attack_ground and enemy.distance_to(position)<enemy.ground_range+1:
            return False
    return True