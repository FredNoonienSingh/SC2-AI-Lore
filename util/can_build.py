from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


def can_build_structure(bot:BotAI, structure_id):
    return bot.can_afford(structure_id) and bot.tech_requirement_progress(structure_id) and not bot.already_pending(structure_id)

def can_build_unit(bot:BotAI, unit_id):
    if unit_id == UnitTypeId.PROBE and len(bot.units(unit_id)) > 66:
        return False
    return bot.can_afford(unit_id) and bot.can_feed(unit_id) and bot.tech_requirement_progress(unit_id)

def can_research_upgrade(bot:BotAI,upgrade_id):
    return False
