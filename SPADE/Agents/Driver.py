from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class Driver(Agent):

    def __init__(self, jid: str, password: str, parking_manager_jid):
        super().__init__(jid, password)
        self.parking_manager_jid = parking_manager_jid
        self.assigned_spot_queue = None
        self.has_park = False
        self.parking_spot_jid = ""
        self.parking_env = ""
        self.parking_pricing = ""
        self.parking_zone_jid = ""
        self.parking_lat = ""
        self.parking_lon = ""

    def set_assigned_spot_queue(self, assigned_spot_queue):
        self.assigned_spot_queue = assigned_spot_queue

    class RequestParkingBehaviour(OneShotBehaviour):
        def __init__(self, owner, lat, lon, environment, price):
            super().__init__()
            self.owner = owner
            self.lat = lat
            self.lon = lon
            self.environment = environment
            self.price = price

        async def run(self):
            # Create a request message
            # Example: "Request Outdoor-Preferred Low 40.7128 -74.0060"
            msg = Message(to=self.owner.parking_manager_jid)
            msg.body = f"Request {self.environment} {self.price} {self.lat} {self.lon}"
            # Send the request message
            await self.send(msg)
            # Wait for the response
            response_msg = await self.receive(timeout=15)  # Adjust the timeout as per your needs
            if response_msg:
                # Process the response
                parking_zone_manager_id = response_msg.body
                print(f"Received parking manager ID: {parking_zone_manager_id}")
                # Create a request message
                msg = Message(to=parking_zone_manager_id)
                msg.body = "Request"
                await self.send(msg)
                response_msg = await self.receive(timeout=15)  # Adjust the timeout as per your needs
                if response_msg:
                    # Process the response
                    parking_spot_id = response_msg.body.split()[0]
                    self.owner.parking_pricing = response_msg.body.split()[1]
                    self.owner.parking_env = response_msg.body.split()[2]
                    self.owner.parking_lat = response_msg.body.split()[3]
                    self.owner.parking_lon = response_msg.body.split()[4]
                    self.owner.parking_zone_jid = str(response_msg.sender)
                    self.owner.parking_spot_jid = parking_spot_id
                    self.owner.has_park = True
                    # Put the assigned spot in the queue
                    if self.owner.assigned_spot_queue is not None:
                        self.owner.assigned_spot_queue.put(parking_spot_id)

    # "Request $environment $pricing $lat $lon"
    async def execute_behaviour2(self, lat: float, lon: float, environment: str, price: str):
        request_behaviour = self.RequestParkingBehaviour(self, lat, lon, environment, price)
        self.add_behaviour(request_behaviour)
