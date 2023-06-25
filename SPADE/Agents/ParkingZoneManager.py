import random
import asyncio
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ParkingZoneManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.current_high_bid = 0
            self.current_winner = None
            self.timestamp = datetime.now()
            self.number_of_poors = 0
            self.vacant_spaces = 0
            self.client = mqtt.Client()
            self.client.connect("localhost", 1883)
            self.driver = ""
            self.current_winner_lat = ""
            self.current_winner_lon = ""

        async def end_auction(self):
            # Mark the auction as ended
            self.owner.auction_in_progress = False
            print("Auction ended.")

            # Notify the bidders about the end of the auction
            winner_bid = self.current_high_bid
            winner_jid = self.current_winner
            self.current_high_bid = 0
            self.current_winner = ""
            await self.notify_bidders(winner_bid, winner_jid)
            response_msg = Message(to=self.driver)
            response_msg.body = f"{winner_jid} {self.owner.price_hour} {self.owner.environment} {self.current_winner_lat} {self.current_winner_lon}"
            await self.send(response_msg)

        async def start_auction(self, vacant_spots):
            self.owner.auction_in_progress = True
            self.timestamp = datetime.now()
            initial_bid = random.randrange(10, 25)  # Set the initial bid value
            for jid in vacant_spots:
                start_msg = Message(to=jid)
                start_msg.body = f"AuctionStart {initial_bid}"
                await self.send(start_msg)

        async def notify_bidders(self, winner_bid, winner_jid):
            for spot in self.owner.find_vacant_parking_spots():
                end_msg = Message(to=spot)
                end_msg.body = f"AuctionEnd {winner_bid} {winner_jid}"
                await self.send(end_msg)

        async def run(self):
            # Wait for incoming messages from ParkingSpotModuleController agents
            msg = await self.receive(timeout=5)  # Adjust the timeout as per your needs

            if msg:
                sender_jid = str(msg.sender)
                vacant_spots = self.owner.find_vacant_parking_spots()

                if msg.body == "Request":
                    # start auction
                    self.driver = sender_jid
                    if vacant_spots:
                        await self.start_auction(vacant_spots)
                    # response = self.owner.find_vacant_parking_spot()
                elif "Bid" in msg.body:
                    # Process the bid
                    if not self.owner.auction_in_progress:
                        return
                    current_bid = int(msg.body.split()[1])
                    print(f"Received bid {current_bid} from {sender_jid}")

                    # Check if the bid is higher than current high bid
                    if current_bid > self.current_high_bid:
                        self.current_high_bid = current_bid
                        self.current_winner = sender_jid
                        self.current_winner_lat = msg.body.split()[2]
                        self.current_winner_lon = msg.body.split()[3]

                        # Increase the bid and ask for new bids
                        new_bid = current_bid + 1
                        for jid in vacant_spots:
                            start_msg = Message(to=jid)
                            start_msg.body = f"BidRequest {new_bid}"
                            await self.send(start_msg)

                    current_time = datetime.now()
                    if current_time >= self.timestamp + timedelta(seconds=2):
                        await self.end_auction()
                elif "Poor" in msg.body:
                    if not self.owner.auction_in_progress:
                        return
                    print(f"{sender_jid} is Poor!!!!")
                    self.number_of_poors += 1
                    if self.number_of_poors >= len(vacant_spots):
                        print("No more money in the cash...")
                        await self.end_auction()
                else:  # TODO: ADD MESSAGE TYPE?
                    # Process the message and update the parking spot status
                    message_parts = msg.body.split()
                    vacancy_status = message_parts[0]

                    if len(message_parts) > 1:
                        try:
                            number = float(message_parts[1])
                            self.send_price(0, number * self.owner.price_hour)
                        except ValueError:
                            pass

                    # Update the parking spot status using the manager's reference
                    self.owner.update_parking_spot_status(sender_jid, vacancy_status)
                    if vacancy_status == "Occupied":
                        self.send_price(1)
                    self.vacant_spaces = self.owner.count_vacant_parking_spots()

                    # Create a message to inform the parking spot manager about the vacancy status
                    info = Message(to=self.owner.manager_jid)  # Replace with the appropriate recipient

                    self.send_display()

                    # send environment information
                    info.body = f"{self.vacant_spaces} {self.owner.lat} {self.owner.lon}" \
                                f" {self.owner.price_hour} {self.owner.environment}"
                    # Send the message
                    await self.send(info)

        def send_display(self):
            self.client.publish(f"{self.owner.pz_id}_display_value", self.vacant_spaces)

        def send_price(self, is_parked, price=""):
            self.client.publish("parked", f"{is_parked} {price}")

    def __init__(self, jid: str, password: str, manager_jid, lat: float, lon: float, price_hour: float, environment: str
                 , pz_id: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.auction_in_progress = False
        self.parking_spots = {}  # Dictionary to store parking spot status
        self.manager_jid = manager_jid
        self.lat = lat
        self.lon = lon
        self.price_hour = price_hour
        self.environment = environment
        self.pz_id = pz_id

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

    def find_vacant_parking_spots(self):
        # Implement your logic to find all vacant parking spots
        # The function now returns a list of all vacant spots
        vacant_spots = []
        for spot, vacancy in self.parking_spots.items():
            if vacancy == "Vacant":
                vacant_spots.append(spot)
        return vacant_spots
