
from sc2.bot_ai import BotAI
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId

def calculate_enemy_supply(bot: BotAI, units:Units=None)-> int:
    if units == None: 
        units = bot.enemy_units.filter(lambda unit: unit.type_id not in [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE])
    return sum([bot.calculate_supply_cost(unit.type_id) for unit in units])
