from spade import agent
import spade
from Agents.ParkingSpotModule import ParkingSpotModule
from Agents.ParkingSpotsManager import ParkingSpotManager


async def main():
    parking_manager = ParkingSpotManager("parking_manager@xavi.lan", "password")
    await parking_manager.start()
    parking_manager.web.start(hostname="xavi.lan", port="10000")
    parking_spot = ParkingSpotModule("parking_spot_1@xavi.lan", "password")
    await parking_spot.start()
    parking_spot.web.start(hostname="xavi.lan", port="10001")

if __name__ == "__main__":
    spade.run(main())

