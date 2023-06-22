
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

def structure_in_proximity(bot:BotAI, checked_structure, structure, max_distance)-> bool:
    structures = bot.structures.closer_than(max_distance,structure)
    structure_names = [structures[x].name for x in range(len(structures))]
    return checked_structure in structure_names
   
def unit_in_proximity(bot:BotAI, checked_unit:str, unit) ->bool:
    units = bot.units.closer_than(5, unit)
    unit_names = [units[x].name for x in range(len(units))]
    return checked_unit in unit_names
