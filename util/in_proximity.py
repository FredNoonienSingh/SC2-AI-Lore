
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

def structure_in_proximity(bot:BotAI, checked_structure, structure)-> bool:
    structures = bot.structures.closer_than(7,structure)
    structure_names = [structures[x].name for x in range(len(structures))]
    return checked_structure in structure_names
   