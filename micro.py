from threading import Thread
from typing import Union

from sc2.bot_ai import BotAI 
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point3

'''Airforce'''
from unit_micro.phoenix_micro import phoenix_micro
from unit_micro.voidray_micro import voidray_micro

'''Ground Units'''
from unit_micro.zealot_micro import zealot_micro
from unit_micro.immortal_micro import immortal_micro
from unit_micro.stalker_micro import stalker_micro

'''Support Units'''
from unit_micro.observer_micro import observer_micro


async def micro(bot: BotAI): 
    
        unit_functions: dict = {
            UnitTypeId.PHOENIX: phoenix_micro, 
            UnitTypeId.VOIDRAY: voidray_micro, 
            UnitTypeId.ZEALOT: zealot_micro, 
            UnitTypeId.STALKER: stalker_micro, 
            UnitTypeId.IMMORTAL: immortal_micro, 
            UnitTypeId.OBSERVER: observer_micro
        }

        for unit_type in unit_functions: 
            await execute_orders(bot, unit_type, unit_functions.get(unit_type))

async def execute_orders(bot, unit_type:UnitTypeId, order:callable):
    for unit in bot.units(unit_type):
        await order(bot, unit)