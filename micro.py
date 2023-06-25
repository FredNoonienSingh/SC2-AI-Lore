
from random import randint

from sc2.bot_ai import BotAI 
from sc2.position import Point3

from sc2.ids.buff_id import BuffId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from actions.stay_out_of_range import stay_out_of_range

'''Airforce'''
from unit_micro.phoenix_micro import phoenix_micro
from unit_micro.voidray_micro import voidray_micro

'''Ground Units'''
from unit_micro.zealot_micro import zealot_micro
from unit_micro.stalker_micro import stalker_micro


async def micro(bot: BotAI): 
    
        enemy_airforce = bot.enemy_units.filter(lambda unit: unit.is_flying == True)
        enemy_ground_units = bot.enemy_units.filter(lambda unit: unit.is_flying == False)


        for phoenix in bot.units(UnitTypeId.PHOENIX):
            await phoenix_micro(bot, phoenix,enemy_airforce,enemy_ground_units)

        for voidray in bot.units(UnitTypeId.VOIDRAY):
            await voidray_micro(bot, voidray, enemy_airforce, enemy_ground_units)

        
        for zealot in bot.units(UnitTypeId.ZEALOT):
           await zealot_micro(bot, zealot, enemy_ground_units)
            
        for stalker in bot.units(UnitTypeId.STALKER):
           await stalker_micro(bot, stalker)
