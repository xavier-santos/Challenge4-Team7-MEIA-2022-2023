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
        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            # Create a request message
            msg = Message(to=self.owner.parking_manager_jid)
            msg.body = "Request"

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
                    # Process the response
                    parking_spot_id = response_msg.body
                    self.owner.parking_spot_jid = parking_spot_id
                    # Put the assigned spot in the queue
                    if self.owner.assigned_spot_queue is not None:
                        self.owner.assigned_spot_queue.put(parking_spot_id)

    async def execute_behaviour(self):
        request_behaviour = self.RequestParkingBehaviour(self)
        self.add_behaviour(request_behaviour)
