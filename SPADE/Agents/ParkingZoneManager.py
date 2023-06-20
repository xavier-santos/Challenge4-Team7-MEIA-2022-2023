import random
from asyncio import asyncio
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ParkingZoneManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.last_bid_time = None
            self.current_high_bid = 0
            self.current_winner = None

        async def run(self):
            # Wait for incoming messages from ParkingSpotModuleController agents
            msg = await self.receive(timeout=5)  # Adjust the timeout as per your needs

            if msg:
                sender_jid = str(msg.sender)
                vacant_spots = self.owner.find_vacant_parking_spot()

                if msg.body == "Request":
                    # start auction
                    if vacant_spots:
                        await self.owner.start_auction(vacant_spots)
                        await asyncio.sleep(5)  # Wait for 5 seconds
                        if self.owner.auction_in_progress:
                            await self.owner.end_auction()  # End the auction if it's not already ended
                    # response = self.owner.find_vacant_parking_spot()
                    # response_msg = Message(to=sender_jid)
                    # response_msg.body = response
                    # await self.send(response_msg)
                elif "Bid" in msg.body:
                    # Process the bid
                    current_bid = int(msg.body.split()[-1])
                    print(f"Received bid {current_bid} from {sender_jid}")

                    # Check if the bid is higher than current high bid
                    if current_bid > self.current_high_bid:
                        self.current_high_bid = current_bid
                        self.current_winner = sender_jid
                        self.last_bid_time = datetime.now()

                        # Increase the bid and ask for new bids
                        new_bid = current_bid + 1
                        for jid in vacant_spots:
                            start_msg = Message(to=jid)
                            start_msg.body = f"BidRequest {new_bid}"
                            await self.send(start_msg)
                else:  # TODO: ADD MESSAGE TYPE?
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
        self.auction_in_progress = False
        self.parking_spots = {}  # Dictionary to store parking spot status
        self.manager_jid = manager_jid

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)

    async def start_auction(self, vacant_spots):
        self.auction_in_progress = True
        initial_bid = random.randrange(10, 25)  # Set the initial bid value
        for jid in vacant_spots:
            start_msg = Message(to=jid)
            start_msg.body = f"AuctionStart {initial_bid}"
            await self.send(start_msg)

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

    def find_vacant_parking_spots(self):
        # Implement your logic to find all vacant parking spots
        # The function now returns a list of all vacant spots
        vacant_spots = []
        for spot, vacancy in self.parking_spots.items():
            if vacancy == "Vacant":
                vacant_spots.append(spot)
        return vacant_spots

    async def end_auction(self):
        # Mark the auction as ended
        self.auction_in_progress = False
        print("Auction ended.")

        # Notify the bidders about the end of the auction
        winner_bid = self.current_high_bid
        winner_jid = self.current_winner
        await self.notify_bidders(winner_bid, winner_jid)

    async def notify_bidders(self, winner_bid, winner_jid):
        for spot, vacancy in self.parking_spots.items():
            if vacancy == "Vacant":
                end_msg = Message(to=spot)
                end_msg.body = f"AuctionEnd {winner_bid} {winner_jid}"
                await self.send(end_msg)
