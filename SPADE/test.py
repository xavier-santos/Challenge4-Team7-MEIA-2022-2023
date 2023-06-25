from pydantic import BaseModel
from fastapi import FastAPI
import random
import paho.mqtt.client as mqtt

app = FastAPI()

broker_address = "localhost"
broker_port = 1883

topic = "pz1_display_value"
topic2 = "pz2_display_value"

client = mqtt.Client()

client.connect(broker_address, broker_port)


class SpotData(BaseModel):
    lat: float
    lon: float


@app.post("/parking_module/{pmodule_id}/{zone_id}")
async def create_spot(pmodule_id: str, zone_id: str, spot_data: SpotData):
    lat = spot_data.lat
    lon = spot_data.lon

    print(f"Received:")
    print(f"Spot Id: {pmodule_id} ")
    print(f"Zone Id: {zone_id} ")
    print(f"Lat: {lat} ")
    print(f"Lon: {lon} ")


class ExecuteBehaviourRequest(BaseModel):
    sonar_value: int


@app.post("/parking_module/{pmodule_id}")
async def send_sonar(pmodule_id: str, request: ExecuteBehaviourRequest):
    sonar_value = request.sonar_value
    print(f"Parking Id Received: {pmodule_id} ")
    print(f"Sonar Value: {sonar_value} ")
    client.publish(topic, f"{random.randint(0, 9)}")
    client.publish(topic2, f"{random.randint(0, 9)}")


if __name__ == "__main__":
    client.publish(topic, f"{random.randint(0, 9)}")
    client.publish(topic2, f"{random.randint(0, 9)}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
