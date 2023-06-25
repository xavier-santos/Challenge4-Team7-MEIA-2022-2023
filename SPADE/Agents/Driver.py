from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class Driver(Agent):

    def __init__(self, jid: str, password: str, parking_manager_jid):
        super().__init__(jid, password)
        self.parking_manager_jid = parking_manager_jid
        self.assigned_spot_queue = None

    def set_assigned_spot_queue(self, assigned_spot_queue):
        self.assigned_spot_queue = assigned_spot_queue

    class RequestParkingBehaviour(OneShotBehaviour):
        def __init__(self, owner, environment, pricing, lat, lon):
            super().__init__()
            self.lon = lon
            self.lat = lat
            self.pricing = pricing
            self.environment = environment
            self.owner = owner

        async def run(self):
            # Create a request message
            msg = Message(to=self.owner.parking_manager_jid)
            msg.body = f"Request {self.environment} {self.pricing} {self.lat} {self.lon}"

            await self.send(msg)
            response_msg = await self.receive(timeout=15)  # Adjust the timeout as per your needs
            if response_msg:
                parking_zone_manager_id = response_msg.body
                print(f"Received parking manager ID: {parking_zone_manager_id}")
                msg = Message(to=parking_zone_manager_id)
                msg.body = "Request"
                await self.send(msg)
                response_msg = await self.receive(timeout=15)  # Adjust the timeout as per your needs
                if response_msg:
                    parking_spot_id = response_msg.body
                    self.owner.parking_spot_jid = parking_spot_id
                    if self.owner.assigned_spot_queue is not None:
                        self.owner.assigned_spot_queue.put(parking_spot_id)

    # "Request $environment $pricing $lat $lon"
    async def execute_behaviour(self, environment, pricing, lat, lon):
        request_behaviour = self.RequestParkingBehaviour(self, environment, pricing, lat, lon)
        self.add_behaviour(request_behaviour)
