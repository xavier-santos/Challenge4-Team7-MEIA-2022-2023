import threading
import asyncio
import spade
import tracemalloc
from queue import Queue
from flask import Flask, request, jsonify

from Agents.Driver import Driver
from Agents.ParkingManager import ParkingManager
from Agents.ParkingSpotModule import ParkingSpotModule
from Agents.ParkingZoneManager import ParkingZoneManager

app = Flask(__name__)
tracemalloc.start()

# Shared data structure for passing information between threads
assigned_spot_queue = Queue()


@app.route("/request-parking-spot", methods=["POST"])
def request_parking_spot():
    # Get the driver JID from the request data
    driver_jid = request.json.get("driver_jid")

    # Create the driver agent
    driver_agent = create_driver_agent(driver_jid)

    # Start the driver agent in the SPADE thread
    spade_thread = threading.Thread(target=start_driver_agent, args=(driver_agent,))
    spade_thread.start()

    # Wait for the assigned spot
    assigned_spot = assigned_spot_queue.get()  # Blocking until an assigned spot is available

    # Return the assigned spot as a JSON response
    return jsonify({"assigned_spot": assigned_spot})


def create_driver_agent(driver_jid):
    driver = Driver(driver_jid, "password", "parking_manager@xavi.lan")  # Replace with the appropriate password
    driver.set_assigned_spot_queue(assigned_spot_queue)  # Pass the shared queue to the driver agent
    return driver


def start_driver_agent(driver_agent):
    asyncio.run(driver_agent.start())


async def main():
    # Start the SPADE agents
    parking_manager = ParkingManager("parking_manager@xavi.lan", "password")
    await parking_manager.start()
    parking_zone_manager = ParkingZoneManager("parking_zone_manager@xavi.lan", "password", "parking_manager@xavi.lan")
    await parking_zone_manager.start()
    parking_spot = ParkingSpotModule("parking_spot_1@xavi.lan", "password", "parking_zone_manager@xavi.lan")
    await parking_spot.start()


if __name__ == "__main__":
    # Create a separate thread for running the SPADE agents
    spade_thread = threading.Thread(target=lambda: spade.run(main()))
    spade_thread.start()

    # Start the Flask application in the main thread
    app.run(port=5000)
