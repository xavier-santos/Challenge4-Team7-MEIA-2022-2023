from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import time


def get_sonar_value():
    # Implement your own method to read the sonar sensor value and return it
    # You can use any library or method to read the sensor value

    # Example implementation using a random value
    import random
    return random.randint(0, 200)


class ParkingSpotModule(Agent):

    def __init__(self, agent_jid, agent_password):
        super().__init__(jid=agent_jid, password=agent_password)

    class InformBehaviour(CyclicBehaviour):
        async def run(self):
            # Read sonar sensor value and determine vacancy based on distance in cm
            sonar_value = get_sonar_value()  # Implement your own method to read the sonar sensor value

            # Determine if the parking spot is vacant based on the sonar value
            is_vacant = sonar_value > 100  # Adjust the threshold according to your specific needs

            # Create a message to inform the parking spot manager about the vacancy status
            msg = Message(to="parking_manager@xavi.lan")  # Replace with the appropriate recipient
            msg.body = "Vacant" if is_vacant else "Occupied"

            # Send the message
            await self.send(msg)

            time.sleep(5)

    async def setup(self):
        inform_behaviour = self.InformBehaviour()
        self.add_behaviour(inform_behaviour)
