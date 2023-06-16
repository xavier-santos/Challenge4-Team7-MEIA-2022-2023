from pydantic import BaseModel
from fastapi import FastAPI
import asyncio

from Agents.Driver import Driver
from Agents.ParkingManager import ParkingManager
from Agents.ParkingSpotModule import ParkingSpotModule
from Agents.ParkingZoneManager import ParkingZoneManager

app = FastAPI()

agents = {}  # to keep track of created agents


@app.post("/parking_module/{pmodule_id}/{zone_id}")
async def create_spot(pmodule_id: str, zone_id: str):
    spot = ParkingSpotModule(f"{pmodule_id}@xavi.lan", "agent_password", f"{zone_id}@xavi.lan")
    await spot.start()
    agents[pmodule_id] = spot
    return {"Agent": pmodule_id, "Status": "Created"}


class ExecuteBehaviourRequest(BaseModel):
    sonar_value: int


@app.post("/parking_module/{pmodule_id}")
async def send_sonar(pmodule_id: str, request: ExecuteBehaviourRequest):
    sonar_value = request.sonar_value
    print("potato")
    if pmodule_id in agents:
        asyncio.create_task(agents[pmodule_id].execute_behaviour(sonar_value))
        return {"Agent": pmodule_id, "Behaviour": "OneShotBehaviour Executed"}
    else:
        return {"Error": "No such agent exists"}


@app.post("/parking_zone/{zone_id}/{manager_id}")
async def create_zone(zone_id: str, manager_id: str):
    zone = ParkingZoneManager(f"{zone_id}@xavi.lan", "agent_password", f"{manager_id}@xavi.lan")
    await zone.start()
    agents[zone_id] = zone
    return {"Agent": zone_id, "Status": "Created"}


@app.post("/parking_manager/{manager_id}")
async def create_zone(manager_id: str):
    manager = ParkingManager(f"{manager_id}@xavi.lan", "agent_password")
    await manager.start()
    agents[manager_id] = manager
    return {"Agent": manager_id, "Status": "Created"}


@app.get("/driver/{driver_id}")
async def execute_behaviour(driver_id: str):
    if driver_id in agents:
        asyncio.create_task(agents[driver_id].execute_behaviour())
        return {"Agent": driver_id, "Behaviour": "OneShotBehaviour Executed"}
    else:
        return {"Error": "No such agent exists"}


@app.post("/driver/{driver_id}")
async def create_driver(driver_id: str):
    driver = Driver(f"{driver_id}@xavi.lan", "agent_password")
    await driver.start()
    agents[driver_id] = driver
    return {"Agent": driver_id, "Status": "Created"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
