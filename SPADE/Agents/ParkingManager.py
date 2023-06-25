from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ParkingManager(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        AVAILABLE_ENVIRONMENTS = ["Outdoor", "Indoor", "Both", "Indoor-Preferred", "Outdoor-Preferred"]
        AVAILABLE_PRICING_OPTIONS = ["Low", "Medium", "High"]

        async def run(self):
            msg = await self.receive(timeout=5)

            if msg:
                sender_jid = str(msg.sender)

                if msg.body.startswith("Request"):
                    environment, pricing, lat, lon = self.extract_request_params(msg.body)
                    response = self.find_vacant_parking_spot(environment, pricing, lat, lon)
                    response_msg = Message(to=sender_jid)
                    response_msg.body = response
                    await self.send(response_msg)
                else:
                    # Process the message and extract the number of vacant spaces
                    vacant_spaces = int(msg.body)
                    self.update_vacant_spaces(sender_jid, vacant_spaces)

        def extract_request_params(self, request_msg):
            # Extract environment, pricing, latitude, and longitude information from the request message
            # Example: "Request Outdoor-Preferred Low 40.7128 -74.0060"
            params = request_msg.split()[1:]  # Remove the "Request" part
            environment = params[0] if params[0] in self.AVAILABLE_ENVIRONMENTS else None
            pricing = params[1] if params[1] in self.AVAILABLE_PRICING_OPTIONS else None
            lat = float(params[2]) if len(params) >= 3 else None
            lon = float(params[3]) if len(params) >= 4 else None
            return environment, pricing, lat, lon

        def update_vacant_spaces(self, parking_manager, vacant_spaces):
            self.owner.vacant_spaces[parking_manager] = vacant_spaces

            print(f"Parking zone manager {parking_manager} has {vacant_spaces} vacant spaces")

        def find_vacant_parking_spot(self, environment=None, pricing=None, lat=None, lon=None):
            matched_spots = []

            # sends message to all to know its environment etc

            for spot, spots in self.owner.vacant_spaces.items():
                if spots > 0:
                    spot_environment, spot_pricing, spot_lat, spot_lon = spot.split()
                    score = self.calculate_score(spot_environment, spot_pricing, spot_lat, spot_lon, environment, pricing, lat, lon)
                    matched_spots.append((spot, score))

            if matched_spots:
                matched_spots.sort(key=lambda x: x[1], reverse=True)
                return matched_spots[0][0]

            return None

        def calculate_score(self, spot_environment, spot_pricing, spot_lat, spot_lon, client_environment, client_pricing, client_lat, client_lon):
            environment_weight = 3 if spot_environment == client_environment else 2 if spot_environment.endswith("-Preferred") else 1
            pricing_weight = 3 if spot_pricing == client_pricing else 2 if spot_pricing == "Low" and client_pricing == "High" else 1
            proximity_weight = self.calculate_proximity_weight(spot_lat, spot_lon, client_lat, client_lon)
            return environment_weight + pricing_weight + proximity_weight

        def calculate_proximity_weight(self, spot_lat, spot_lon, client_lat, client_lon):
            if spot_lat is not None and spot_lon is not None and client_lat is not None and client_lon is not None:
                distance = self.calculate_distance(spot_lat, spot_lon, client_lat, client_lon)
                if distance <= 0.1:  # 100 meters
                    return 6
                elif distance <= 0.25:  # 250 meters
                    return 5
                elif distance <= 0.5:  # 500 meters
                    return 4
                elif distance <= 1.0:  # 1 kilometer
                    return 3
                elif distance <= 2.0:  # 2 kilometers
                    return 2
                elif distance <= 5.0:  # 5 kilometers
                    return 1
                else:
                    return 0
            else:
                return 0

        def calculate_distance(self, lat1, lon1, lat2, lon2):
            from math import radians, sin, cos, sqrt, atan2

            lat1_rad = radians(lat1)
            lon1_rad = radians(lon1)
            lat2_rad = radians(lat2)
            lon2_rad = radians(lon2)

            earth_radius = 6371.0

            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad
            a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = earth_radius * c

            return distance

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.vacant_spaces = {}  # Dictionary to store vacant space counts for parking spot managers

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)
