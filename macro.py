from sc2.bot_ai import BotAI
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

"""actions"""
from actions.set_rally import set_rally
from actions.abilities import chronoboost
from actions.train_unit import train_unit, warp_in_unit
from actions.build_structure import build_gas, build_structure

'''constants'''

from constants.robo_units import ROBO_UNITS
from constants.nexus_units import NEXUS_UNITS
from constants.gateway_units import GATEWAY_UNITS
from constants.stargate_units import STARGATE_UNITS
from constants.buildings import PROTOSS_BUILDINGS as BUILDINGS

"""custom util"""
from util.in_proximity import structure_in_proximity
from util.calculate_supply import calculate_enemy_supply
from util.can_build import can_build_unit, can_build_structure


async def macro(bot:BotAI):
        MAX_DISTANCE = 10
        if bot.townhalls and bot.units:
            await bot.distribute_workers(resource_ratio=2)
           
           
            build_pos = bot.main_base_ramp.protoss_wall_pylon.towards(bot.game_info.map_center)
            if bot.structures(UnitTypeId.PYLON):
                #keep in mind:"in_closest_distance_to_group"
                warp_in_pos = bot.structures(UnitTypeId.PYLON).closest_to(bot.enemy_start_locations[0])
            worker = bot.workers.prefer_idle.closest_to(build_pos) 

            #chrono_nexus = bot.structures(UnitTypeId.NEXUS).filter(lambda nexus: nexus.energy > 50).closest_to(build_pos)

            if bot.step<len(bot.build_order):
                next_step = bot.build_order[bot.step]
                
            prod_structure = None
            if next_step[0] in GATEWAY_UNITS:
                prod_structure = UnitTypeId.GATEWAY
            elif next_step[0] in ROBO_UNITS:
                prod_structure = UnitTypeId.ROBOTICSFACILITY
            elif next_step[0] in STARGATE_UNITS:
                prod_structure = UnitTypeId.STARGATE
            elif next_step[0] in NEXUS_UNITS:
                prod_structure = UnitTypeId.NEXUS
            
            if prod_structure is not None:
                for gate in bot.structures(prod_structure):#.filter(lambda structure: structure):
                    if prod_structure == UnitTypeId.GATEWAY:
                       result = await  warp_in_unit(bot, next_step[0], warp_in_pos)
                       return
                    result = await train_unit(bot,next_step[0],gate)
                    if result: 
                        if next_step[1]:
                            pass
                            #await chronoboost(bot, chrono_nexus, prod_structure)
                        bot.step += 1
                    break
             
            elif next_step[0] in BUILDINGS:
                if can_build_structure(bot,next_step[0]):
                    if await build_structure(bot,next_step[0],build_pos,worker):
                        if bot.debug:
                            print(f"build {next_step[0]}")
                        bot.step += 1

            elif next_step[0] == UnitTypeId.ASSIMILATOR:
                if can_build_structure(bot, UnitTypeId.ASSIMILATOR):
                    if await build_gas(bot, bot.structures(UnitTypeId.NEXUS).closest_to(build_pos)):
                        bot.step += 1

            elif next_step[0] == UnitTypeId.NEXUS:
                if can_build_structure(bot,UnitTypeId.NEXUS):
                    await bot.expand_now()
                    bot.step += 1