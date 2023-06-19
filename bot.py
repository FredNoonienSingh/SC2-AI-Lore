from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.ids.buff_id import BuffId
from sc2.ids.ability_id import AbilityID
from sc2.ids.unit_typeid import UNitTypeId


class HalBot(BotAI):
    def __init__(self, debug_mode:bool=False)->None:
        super().__init__()

        self.name = "HalBot"
        self.version = "0.1"
        self.race = Race.Protoss

    async def on_start(self)-> None:
        await self.chat_send(f"I am {self.name} v.{self.version}")

    async def on_step(self) -> None:
        if self.townhalls:
            pass 


