from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class ParkingSpotManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, manager):
            super().__init__()
            self.manager = manager

        async def run(self):
            # Wait for incoming messages from ParkingSpotModule agents
            msg = await self.receive(timeout=5)  # Adjust the timeout as per your needs

            if msg:
                # Process the message and update the parking spot status
                parking_module = msg.sender.localpart  # Extract the parking spot module's name from the sender's JID
                vacancy_status = msg.body

                # Update the parking spot status using the manager's reference
                self.manager.update_parking_spot_status(parking_module, vacancy_status)

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.parking_spots = {}  # Dictionary to store parking spot status

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)

    def update_parking_spot_status(self, parking_module, vacancy_status):
        # Update the parking spot status in the manager's internal data structure (dictionary)
        self.parking_spots[parking_module] = vacancy_status

        # Print the updated status
        print(f"Parking spot {parking_module} is {vacancy_status}")
