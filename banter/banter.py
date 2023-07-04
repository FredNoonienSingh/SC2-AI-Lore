
from sc2.data import Race
from sc2.unit import Unit 
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


async def greeting(bot:BotAI): 

    if bot.enemy_race == Race.Terran:
        race = "Terran"
    if bot.enemy_race == Race.Protoss:
        race = "Protoss"
    if bot.enemy_race == Race.Zerg:
        race = "Zerg"

    await bot.chat_send(f"i am {bot.name} Version {bot.version}")
    await bot.chat_send(f"I see you are playing {race}, i have something against that")

async def looser_bot_taunt(bot:BotAI):

    if bot.enemy.name == "LucidTJS":
        await bot.chat_send(f"Lol - {bot.enemy.name} --- JS-TrashBot ... you pathic looser ... hahahahaha")