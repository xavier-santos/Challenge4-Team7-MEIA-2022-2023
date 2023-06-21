import asyncio
import random

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class ParkingSpotModule(Agent):

    def __init__(self, agent_jid, agent_password, manager_jid):
        super().__init__(jid=agent_jid, password=agent_password)
        self.manager_jid = manager_jid
        self.cash = random.randrange(100, 200)
        self.private_value = None

    class InformBehaviour(OneShotBehaviour):

        def __init__(self, owner, sonar_value):
            super().__init__()
            self.owner = owner
            self.sonar_value = sonar_value

        async def run(self):
            # Determine if the parking spot is vacant based on the sonar value
            is_vacant = self.sonar_value > 30  # Adjust the threshold according to your specific needs
            # Create a message to inform the parking spot manager about the vacancy status
            msg = Message(to=self.owner.manager_jid)  # Replace with the appropriate recipient
            msg.body = "Vacant" if is_vacant else "Occupied"
            # Send the message
            await self.send(msg)

    class BidBehaviour(CyclicBehaviour):

        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                if "AuctionStart" in msg.body:
                    self.owner.private_value = random.randrange(30, 45)
                    if self.owner.private_value > self.owner.cash:
                        self.owner.private_value = self.owner.cash

                    initial_bid = int(msg.body.split()[-1])

                    if self.owner.private_value > initial_bid:
                        # Send initial bid
                        bid_msg = Message(to=self.owner.manager_jid)
                        bid_msg.body = f"Bid {initial_bid}"  # Here, 1 is the initial bid value. Adjust as needed.
                        await self.send(bid_msg)
                elif "BidRequest" in msg.body:
                    # Increase bid
                    random_step = random.randrange(1, 5)
                    current_bid = int(msg.body.split()[-1])
                    new_bid = current_bid + random_step  # Increase the bid by 1. Adjust as needed.
                    if self.owner.cash >= new_bid & new_bid <= self.owner.private_value:
                        bid_msg = Message(to=self.owner.manager_jid)
                        bid_msg.body = f"Bid {new_bid}"
                        await self.send(bid_msg)
                elif "AuctionEnd" in msg.body:
                    # Auction end logic here (e.g., perform actions after the auction ends)
                    winner_bid, winner_jid = msg.body.split()[1:]
                    if self.owner.jid == winner_jid:
                        self.owner.cash -= int(winner_bid)
                        print(f"Updated cash ({winner_jid}: {self.owner.cash}")

    async def setup(self):
        bid_behaviour = self.BidBehaviour(self)
        self.add_behaviour(bid_behaviour)

    async def execute_behaviour(self, sonar_value: int):
        inform_behaviour = self.InformBehaviour(self, sonar_value)
        self.add_behaviour(inform_behaviour)
