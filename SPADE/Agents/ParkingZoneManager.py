from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ParkingZoneManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            # Wait for incoming messages from ParkingSpotModuleController agents
            msg = await self.receive(timeout=5)  # Adjust the timeout as per your needs

            if msg:
                sender_jid = str(msg.sender)

                if msg.body == "Request":
                    response = self.owner.find_vacant_parking_spot()
                    response_msg = Message(to=sender_jid)
                    response_msg.body = response
                    await self.send(response_msg)
                else:
                    # Process the message and update the parking spot status
                    vacancy_status = msg.body

                    # Update the parking spot status using the manager's reference
                    self.owner.update_parking_spot_status(sender_jid, vacancy_status)

                    # Create a message to inform the parking spot manager about the vacancy status
                    info = Message(to=self.owner.manager_jid)  # Replace with the appropriate recipient
                    info.body = str(self.owner.count_vacant_parking_spots())

                    # Send the message
                    await self.send(info)

    def __init__(self, jid: str, password: str, manager_jid, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.parking_spots = {}  # Dictionary to store parking spot status
        self.manager_jid = manager_jid

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)

    def update_parking_spot_status(self, parking_module, vacancy_status):
        # Update the parking spot status in the manager's internal data structure (dictionary)
        self.parking_spots[parking_module] = vacancy_status

        # Print the updated status
        print(f"Parking spot {parking_module} is {vacancy_status}")

    def count_vacant_parking_spots(self):
        vacant_count = 0
        for status in self.parking_spots.values():
            if status == "Vacant":
                vacant_count += 1
        return vacant_count

    def find_vacant_parking_spot(self):
        # Implement your logic to find a vacant parking spot
        # Example: Return the first vacant spot found
        for spot, vacancy in self.parking_spots.items():
            if vacancy == "Vacant":
                return spot
        return None
