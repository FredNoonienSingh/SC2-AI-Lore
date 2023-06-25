
from sc2.bot_ai import BotAI 
from sc2.position import Point3

from sc2.ids.buff_id import BuffId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from actions.stay_out_of_range import stay_out_of_range
from actions.abilities import *


async def micro(bot: BotAI): 
    

        enemy_ground_units = bot.enemy_units.filter(lambda unit: unit.is_flying == False)
        enemy_airforce = bot.enemy_units.filter(lambda unit: unit.is_flying == True)

        for phoenix in bot.units(UnitTypeId.PHOENIX):
            if phoenix.is_idle and enemy_airforce: 
                enemy = enemy_airforce.closest_to(phoenix)
                phoenix.attack(enemy)
            else:
                await stay_out_of_range(bot, phoenix)

        for voidray in bot.units(UnitTypeId.VOIDRAY):
            if voidray.is_idle and enemy_airforce: 
                enemy = enemy_airforce.closest_to(voidray)
                if enemy.is_armored:
                    prismaticaligment(bot,voidray)
                voidray.attack(enemy)
                if bot.debug: 
                    bot.client.debug_line_out(voidray, enemy, (0,255,255))
            elif voidray.is_idle and enemy_ground_units:
                enemy = enemy_ground_units.closest_to(voidray)
                voidray.attack(enemy)
                if bot.debug: 
                    bot.client.debug_line_out(voidray, enemy, (0,255,255))
        for zealot in bot.units(UnitTypeId.ZEALOT):
            if zealot.is_idle and enemy_ground_units:
                enemy = enemy_ground_units.closest_n_units(zealot, 5)[0]
                zealot.attack(enemy)
            if zealot.shield_percentage < 0.75:
                await stay_out_of_range(bot, zealot)
            
        for stalker in bot.units(UnitTypeId.STALKER):
            if stalker.is_idle and enemy_ground_units:
                enemy = enemy_ground_units.closest_n_units(stalker, 5)[0]
                stalker.attack(enemy)
            if stalker.shield_percentage < 0.5 and enemy_ground_units :
                enemy = enemy_ground_units.closest_n_units(stalker, 5)[0]
                stalker.move(stalker.position.towards(enemy, -1))
            if len(bot.units(UnitTypeId.ZEALOT))+len(bot.units(UnitTypeId.STALKER))>100:
                stalker.attack(bot.enemy_start_locations[0])
                zealot.attack(bot.enemy_start_locations[0])
