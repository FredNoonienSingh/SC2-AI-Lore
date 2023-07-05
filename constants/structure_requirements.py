from sc2.ids.unit_typeid import UnitTypeId

STRUCTURE_REQUIREMENTS: dict = {
    UnitTypeId.NEXUS: [],
    UnitTypeId.PYLON: [],
    UnitTypeId.ASSIMILATOR: [],
    UnitTypeId.GATEWAY: [UnitTypeId.PYLON], 
    UnitTypeId.CYBERNETICSCORE: [UnitTypeId.PYLON, UnitTypeId.GATEWAY], 
    UnitTypeId.FORGE: [UnitTypeId.PYLON],
    UnitTypeId.STARGATE: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE], 
    UnitTypeId.FLEETBEACON: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE, UnitTypeId.STARGATE], 
    UnitTypeId.ROBOTICSFACILITY: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.ROBOTICSBAY: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE, UnitTypeId.ROBOTICSFACILITY],
    UnitTypeId.DARKSHRINE: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE, UnitTypeId.TWILIGHTCOUNCIL],
    UnitTypeId.TWILIGHTCOUNCIL: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.SHIELDBATTERY: [UnitTypeId.PYLON, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.PHOTONCANNON: [UnitTypeId.PYLON, UnitTypeId.FORGE], 
    UnitTypeId.TEMPLARARCHIVE: [UnitTypeId.PYLON, UnitTypeId.TWILIGHTCOUNCIL]
    }

UNIT_REQUIREMENTS: dict = {
    UnitTypeId.PROBE: [], 
    UnitTypeId.ZEALOT: [UnitTypeId.GATEWAY],
    UnitTypeId.ADEPT: [UnitTypeId.GATEWAY, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.DARKTEMPLAR: [UnitTypeId.GATEWAY, UnitTypeId.DARKSHRINE], 
    UnitTypeId.SENTRY: [UnitTypeId.GATEWAY, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.STALKER: [UnitTypeId.GATEWAY, UnitTypeId.CYBERNETICSCORE],
    UnitTypeId.HIGHTEMPLAR: [UnitTypeId.GATEWAY, UnitTypeId.TEMPLARARCHIVE], 
    UnitTypeId.OBSERVER: [UnitTypeId.ROBOTICSFACILITY], 
    UnitTypeId.IMMORTAL: [UnitTypeId.ROBOTICSFACILITY], 
    UnitTypeId.WARPPRISM: [UnitTypeId.ROBOTICSFACILITY], 
    UnitTypeId.COLOSSUS: [UnitTypeId.ROBOTICSFACILITY, UnitTypeId.ROBOTICSBAY], 
    UnitTypeId.DISRUPTOR: [UnitTypeId.ROBOTICSFACILITY, UnitTypeId.ROBOTICSBAY], 
    UnitTypeId.ORACLE: [UnitTypeId.STARGATE], 
    UnitTypeId.PHOENIX: [UnitTypeId.STARGATE], 
    UnitTypeId.VOIDRAY: [UnitTypeId.STARGATE], 
    UnitTypeId.TEMPEST: [UnitTypeId.STARGATE, UnitTypeId.FLEETBEACON], 
    UnitTypeId.CARRIER: [UnitTypeId.STARGATE, UnitTypeId.FLEETBEACON]
}