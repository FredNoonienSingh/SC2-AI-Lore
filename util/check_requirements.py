from sc2.bot_ai import BotAI

def check_requirements(bot: BotAI, requirements:list) -> bool:
    for req in [bot.structures(req) for req in requirements]:
        if not req.ready:
            return False
    return True