from sc2 import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point3

class ArmyGroup:

    def __init__(self, composition:dict, army_type:str) -> None:
        self.army_type = army_type
        self.composition = composition
        self.complete = False 
        self.health = 0
        self.position = Point3((0,0,0))
        self.unit_types = self.composition.keys()
        self.units = self.create_units_dict(self)
        self.losses = []

    def create_units_dict(self) -> dict:
        return {key:[] for key in self.unit_types}

    def check_complete(self):
        for unit_type in self.unit_types:
            if not self.composition.get(unit_type) == len(self.units.get(unit_type)):
                return False
        return True
    
    def add_unit(self, unit: Unit):
        self.units.get(unit.name).append(unit)

    def calc_health(self) -> float:
        # grouphealth = sum(health)/len(units)
        pass 

    def calc_position(self):
        # find the center of the formation 
        pass

    def update(self):
        self.complete = self.check_complete()
        self.health = self.calc_health()
        self.position = self.calc_position()