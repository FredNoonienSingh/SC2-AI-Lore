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
from actions.build_structure import build_gas


async def macro(bot:BotAI):

        if bot.townhalls:
            await bot.distribute_workers(resource_ratio=2)
            max_distance = 10
            for nexus in bot.townhalls:
                if bot.debug:
                    bot.client.debug_sphere_out(nexus ,10, (0,255,0))

                if nexus.surplus_harvesters < 0: 
                    if can_build_unit(bot,UnitTypeId.PROBE) and not nexus.is_active:
                        nexus.train(UnitTypeId.PROBE)
                
                if can_build_structure(bot, UnitTypeId.ASSIMILATOR):
                   await build_gas(bot, nexus)

                build_pos = nexus.position.towards(bot.game_info.map_center)
                
                if not structure_in_proximity(bot, "Pylon", nexus, max_distance) and len(bot.structures(UnitTypeId.PYLON))>1:
                    if can_build_structure(bot,UnitTypeId.PYLON):
                        await bot.build(UnitTypeId.PYLON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))

                if structure_in_proximity(bot, "Pylon", nexus, max_distance):
                    if bot.structures(UnitTypeId.FORGE) and not structure_in_proximity(bot, "PhotonCannon", nexus, max_distance):
                       if can_build_structure(bot, UnitTypeId.PHOTONCANNON):
                            await bot.build(UnitTypeId.PHOTONCANNON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))

            build_pos = bot.main_base_ramp.protoss_wall_pylon.towards(bot.game_info.map_center)
            
            if not bot.structures(UnitTypeId.GATEWAY): 
                if can_build_structure(bot, UnitTypeId.GATEWAY):
                    build_pos = bot.main_base_ramp.protoss_wall_warpin.towards(bot.game_info.map_center)
                    await bot.build(UnitTypeId.GATEWAY,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))                
            
            if can_build_structure(bot, UnitTypeId.FORGE) and bot.structures(UnitTypeId.GATEWAY):
                
                if not bot.structures(UnitTypeId.FORGE):
                    build_pos = bot.main_base_ramp.protoss_wall_warpin.towards(bot.game_info.map_center)
                    await bot.build(UnitTypeId.FORGE,near=build_pos)
            
            if can_build_structure(bot, UnitTypeId.PYLON) and bot.supply_left<3 and not bot.supply_cap == 200:
                await bot.build(UnitTypeId.PYLON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))

            if not bot.structures(UnitTypeId.CYBERNETICSCORE):
                
                if can_build_structure(bot, UnitTypeId.CYBERNETICSCORE):
                    await bot.build(UnitTypeId.CYBERNETICSCORE, near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))

            if bot.structures(UnitTypeId.GATEWAY) and bot.structures(UnitTypeId.CYBERNETICSCORE):
                if not bot.structures(UnitTypeId.TWILIGHTCOUNCIL):
                    if can_build_structure(bot, UnitTypeId.TWILIGHTCOUNCIL):
                        await bot.build(UnitTypeId.TWILIGHTCOUNCIL, near=build_pos)
            
            for council in bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready:
                if bot.can_afford(UpgradeId.CHARGE) and not bot.already_pending_upgrade(UpgradeId.CHARGE):
                    council.research(UpgradeId.CHARGE)

                if not bot.structures(UnitTypeId.STARGATE):
                    if can_build_structure(bot, UnitTypeId.STARGATE):
                        await bot.build(UnitTypeId.STARGATE, near=build_pos)
            
            for gate in bot.structures(UnitTypeId.GATEWAY):
                
                #if can_build_unit(bot, UnitTypeId.STALKER) and not gate.is_active:
                 #   gate.train(UnitTypeId.STALKER)
                
                if can_build_unit(bot, UnitTypeId.ZEALOT) and not gate.is_active:
                    gate.train(UnitTypeId.ZEALOT)

            for gate in bot.structures(UnitTypeId.STARGATE):
                #ship = UnitTypeId.PHOENIX if len(bot.units(UnitTypeId.PHOENIX)) == 0 or len(bot.units(UnitTypeId.VOIDRAY)) >= len(bot.units(UnitTypeId.PHOENIX)) else UnitTypeId.VOIDRAY 
                if can_build_unit(bot,UnitTypeId.VOIDRAY):
                    gate.train(UnitTypeId.VOIDRAY)

            if can_build_structure(bot,UnitTypeId.NEXUS):
                await bot.expand_now()