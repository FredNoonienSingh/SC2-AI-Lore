from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human
from sc2.position import Point3
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId


"""custom util"""
from util.army_group import ArmyGroup
from util.can_build import can_build_unit, can_build_structure
from util.in_proximity import unit_in_proximity, structure_in_proximity

"""actions"""
from actions.set_rally import set_rally
from actions.build_structure import build_gas
from actions.abilities import chronoboost

async def macro(bot:BotAI):
    center = bot.game_info.map_center
    if can_build_structure(bot, UnitTypeId.PYLON):
        if not bot.structures(UnitTypeId.PYLON):
            build_pos =  bot.main_base_ramp.protoss_wall_pylon.towards(center)

        else:
            pylons = bot.structures(UnitTypeId.PYLON).sorted(lambda unit: unit.age_in_frames,reverse=True) 
            build_pos = pylons[0].position.towards(pylons[0],-1)



        await bot.build(UnitTypeId.PYLON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))