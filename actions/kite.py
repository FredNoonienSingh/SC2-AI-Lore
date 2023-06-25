from sc2.unit import Unit
from sc2.position import Point3

async def kite(unit:Unit, enemy: Unit):
    position : Point3 = unit.position.towards(enemy, -2)
    
    if unit.weapon_cooldown >0:
        unit.move(position)
    elif unit.weapon_ready:
        unit.attack(enemy)