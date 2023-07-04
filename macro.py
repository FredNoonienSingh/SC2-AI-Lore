from sc2.bot_ai import BotAI
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

"""custom util"""
from util.in_proximity import structure_in_proximity
from util.calculate_supply import calculate_enemy_supply
from util.can_build import can_build_unit, can_build_structure

"""actions"""
from actions.set_rally import set_rally
from actions.abilities import chronoboost
from actions.build_structure import build_gas
from actions.train_unit import train_unit, warp_in_unit
'''constants'''
from constants.robo_units import ROBO_UNITS
from constants.nexus_units import NEXUS_UNITS
from constants.gateway_units import GATEWAY_UNITS
from constants.stargate_units import STARGATE_UNITS


async def macro(bot:BotAI):

        if bot.townhalls and bot.units:
            await bot.distribute_workers(resource_ratio=2)
            MAX_DISTANCE = 10
            for nexus in bot.townhalls.ready:
                for gate in bot.structures(UnitTypeId.GATEWAY):
                    if gate.is_active and not gate.buffs:
                        await chronoboost(bot, nexus, gate)
                if bot.debug:
                    bot.client.debug_sphere_out(nexus ,10, (0,255,0))

                if nexus.surplus_harvesters < 0: 
                    if can_build_unit(bot,UnitTypeId.PROBE) and not nexus.is_active:
                        nexus.train(UnitTypeId.PROBE)
                
                if len(bot.townhalls)>1:
                    if not bot.structures(UnitTypeId.ASSIMILATOR) or bot.structures(UnitTypeId.CYBERNETICSCORE):
                        if can_build_structure(bot, UnitTypeId.ASSIMILATOR):
                            await build_gas(bot, nexus)

                build_pos = nexus.position.towards(bot.game_info.map_center)
            
                if not structure_in_proximity(bot, "Pylon", nexus, MAX_DISTANCE):
                    if can_build_structure(bot,UnitTypeId.PYLON):
                        await bot.build(UnitTypeId.PYLON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))
                
                if len(bot.townhalls)<2:
                    if can_build_structure(bot,UnitTypeId.NEXUS):
                        await bot.expand_now()
                    return 

                if structure_in_proximity(bot, "Pylon", nexus, MAX_DISTANCE):
                    if bot.structures(UnitTypeId.FORGE) and not structure_in_proximity(bot, "PhotonCannon", nexus, MAX_DISTANCE):
                       if can_build_structure(bot, UnitTypeId.PHOTONCANNON):
                            await bot.build(UnitTypeId.PHOTONCANNON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))
             
            build_pos = bot.main_base_ramp.protoss_wall_pylon.towards(bot.game_info.map_center)
             
            if  not bot.structures(UnitTypeId.GATEWAY): 
                if can_build_structure(bot, UnitTypeId.GATEWAY):
                    build_pos = bot.main_base_ramp.protoss_wall_warpin.towards(bot.game_info.map_center)
                    await bot.build(UnitTypeId.GATEWAY,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))
             
            if can_build_structure(bot, UnitTypeId.FORGE) and bot.structures(UnitTypeId.GATEWAY):
                
                if not bot.structures(UnitTypeId.FORGE):
                    build_pos = bot.main_base_ramp.protoss_wall_warpin.towards(bot.game_info.map_center)
                    await bot.build(UnitTypeId.FORGE,near=build_pos)
             
            if can_build_structure(bot, UnitTypeId.PYLON) and bot.supply_left<5 and not bot.supply_cap == 200:
                await bot.build(UnitTypeId.PYLON,near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))
             
            if not bot.structures(UnitTypeId.CYBERNETICSCORE):
                
                if can_build_structure(bot, UnitTypeId.CYBERNETICSCORE):
                    await bot.build(UnitTypeId.CYBERNETICSCORE, near=build_pos,build_worker=bot.workers.prefer_idle.closest_to(build_pos))
             
            if bot.structures(UnitTypeId.GATEWAY) and bot.structures(UnitTypeId.CYBERNETICSCORE):
                if not bot.structures(UnitTypeId.TWILIGHTCOUNCIL):
                    if can_build_structure(bot, UnitTypeId.TWILIGHTCOUNCIL):
                        await bot.build(UnitTypeId.TWILIGHTCOUNCIL, near=build_pos)
            
            if can_build_structure(bot,UnitTypeId.ROBOTICSFACILITY) and not bot.structures(UnitTypeId.ROBOTICSFACILITY):
                build_pos = bot.structures(UnitTypeId.NEXUS).closest_to(bot.enemy_start_locations[0])
                await bot.build(UnitTypeId.ROBOTICSFACILITY, near=build_pos)

            for council in bot.structures(UnitTypeId.TWILIGHTCOUNCIL).ready:
                if bot.can_afford(UpgradeId.BLINKTECH) and not bot.already_pending_upgrade(UpgradeId.BLINKTECH):
                    council.research(UpgradeId.BLINKTECH)
                if bot.can_afford(UpgradeId.CHARGE) and not bot.already_pending_upgrade(UpgradeId.CHARGE):
                    if council.is_idle:
                        council.research(UpgradeId.CHARGE)

                if not bot.structures(UnitTypeId.STARGATE):
                    if can_build_structure(bot, UnitTypeId.STARGATE):
                        await bot.build(UnitTypeId.STARGATE, near=build_pos)

            for robo in bot.structures(UnitTypeId.ROBOTICSFACILITY):
                if can_build_unit(bot, UnitTypeId.OBSERVER) and not bot.units(UnitTypeId.OBSERVER):
                    robo.train(UnitTypeId.OBSERVER)
                if can_build_unit(bot, UnitTypeId.IMMORTAL) and not bot.units(UnitTypeId.IMMORTAL):
                    robo.train(UnitTypeId.IMMORTAL)

            for gate in bot.structures(UnitTypeId.GATEWAY):
                if can_build_unit(bot, UnitTypeId.STALKER) and not gate.is_active:
                    gate.train(UnitTypeId.STALKER)
                
                stalkers_arr = bot.units(UnitTypeId.STALKER)
                if stalkers_arr:
                    await set_rally(bot, gate, stalkers_arr[0])
                if can_build_unit(bot, UnitTypeId.ZEALOT) and not gate.is_active:
                    gate.train(UnitTypeId.ZEALOT)

            for gate in bot.structures(UnitTypeId.STARGATE):
                ship = UnitTypeId.PHOENIX if len(bot.units(UnitTypeId.PHOENIX)) == 0 or len(bot.units(UnitTypeId.VOIDRAY)) >= len(bot.units(UnitTypeId.PHOENIX)) else UnitTypeId.VOIDRAY 
                if can_build_unit(bot,ship) and not gate.is_active:
                    gate.train(ship)

            if can_build_structure(bot,UnitTypeId.NEXUS):
                await bot.expand_now()
            
            if bot.debug:
                bot.client.debug_text_simple(str(calculate_enemy_supply(bot)))