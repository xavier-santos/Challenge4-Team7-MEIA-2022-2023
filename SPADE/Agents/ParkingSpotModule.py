from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class ParkingSpotModule(Agent):

    def __init__(self, agent_jid, agent_password, manager_jid):
        super().__init__(jid=agent_jid, password=agent_password)
        self.manager_jid = manager_jid

    class InformBehaviour(OneShotBehaviour):

        def __init__(self, owner, sonar_value):
            super().__init__()
            self.owner = owner
            self.sonar_value = sonar_value

        async def run(self):
            # Determine if the parking spot is vacant based on the sonar value
            is_vacant = self.sonar_value > 100  # Adjust the threshold according to your specific needs

            # Create a message to inform the parking spot manager about the vacancy status
            msg = Message(to=self.owner.manager_jid)  # Replace with the appropriate recipient
            msg.body = "Vacant" if is_vacant else "Occupied"

            # Send the message
            await self.send(msg)

    class BidBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                if msg.body == "AuctionStart":
                    # Send initial bid
                    bid_msg = Message(to=self.owner.manager_jid)
                    bid_msg.body = "InitialBid 1"  # Here, 1 is the initial bid value. Adjust as needed.
                    await self.send(bid_msg)
                elif "BidRequest" in msg.body:
                    # Increase bid
                    current_bid = int(msg.body.split()[-1])
                    new_bid = current_bid + 1  # Increase the bid by 1. Adjust as needed.
                    bid_msg = Message(to=self.owner.manager_jid)
                    bid_msg.body = f"Bid {new_bid}"
                    await self.send(bid_msg)

    # TODO: GENERATE PRIVATE VALUATION? ADD MAX VALUE?
    async def execute_behaviour(self, sonar_value: int):
        inform_behaviour = self.InformBehaviour(self, sonar_value)
        self.add_behaviour(inform_behaviour)
