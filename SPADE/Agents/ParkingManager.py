from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ParkingManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            # Wait for incoming messages from ParkingSpotManager agents
            msg = await self.receive(timeout=5)  # Adjust the timeout as per your needs

            if msg:
                sender_jid = str(msg.sender)

                if msg.body == "Request":
                    response = self.find_vacant_parking_spot()
                    response_msg = Message(to=sender_jid)
                    response_msg.body = response
                    await self.send(response_msg)
                else:
                    # Process the message and extract the number of vacant spaces
                    vacant_spaces = int(msg.body)  # Assuming the message body contains the number of vacant spaces as an integer
                    # Update the city's internal data structure with the number of vacant spaces for the parking spot manager
                    self.update_vacant_spaces(sender_jid, vacant_spaces)

        def update_vacant_spaces(self, parking_manager, vacant_spaces):
            # Update the city's internal data structure (dictionary, list, etc.) with the number of vacant spaces for the parking spot manager
            # You can choose an appropriate data structure based on your requirements
            # For example, you can use a dictionary with parking manager names as keys and vacant space counts as values
            self.owner.vacant_spaces[parking_manager] = vacant_spaces

            # Print the updated vacant space count for the parking spot manager
            print(f"Parking zone manager {parking_manager} has {vacant_spaces} vacant spaces")

        def find_vacant_parking_spot(self):
            # Implement your logic to find a vacant parking spot
            # Example: Return the first vacant spot found
            for spot, spots in self.owner.vacant_spaces.items():
                if spots > 0:
                    return spot
            return None

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.vacant_spaces = {}  # Dictionary to store vacant space counts for parking spot managers

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)
