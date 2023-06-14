from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


def get_sonar_value():
    # Implement your own method to read the sonar sensor value and return it
    # You can use any library or method to read the sensor value

    # Example implementation using a random value
    import random
    return random.randint(0, 200)


class ParkingSpotModule(Agent):

    def __init__(self, agent_jid, agent_password, manager_jid):
        super().__init__(jid=agent_jid, password=agent_password)
        self.manager_jid = manager_jid

    class InformBehaviour(OneShotBehaviour):

        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            # Read sonar sensor value and determine vacancy based on distance in cm
            sonar_value = get_sonar_value()  # Implement your own method to read the sonar sensor value

            # Determine if the parking spot is vacant based on the sonar value
            is_vacant = sonar_value > 100  # Adjust the threshold according to your specific needs

            # Create a message to inform the parking spot manager about the vacancy status
            msg = Message(to=self.owner.manager_jid)  # Replace with the appropriate recipient
            msg.body = "Vacant"

            # Send the message
            await self.send(msg)

    async def setup(self):
        inform_behaviour = self.InformBehaviour(self)
        self.add_behaviour(inform_behaviour)
