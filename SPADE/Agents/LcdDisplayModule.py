import paho.mqtt.client as mqtt
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class LcdDisplayModule(Agent):
    class ListenBehaviour(CyclicBehaviour):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.vacant_spaces = 0
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.connect("localhost", 1883)
            client.loop_start()
            client.loop_stop()
            client.disconnect()

        async def run(self):
            msg = await self.receive(timeout=5)

            if msg:
                self.vacant_spaces = int(msg.body)
                client = mqtt.Client()
                client.on_connect = self.on_connect
                client.connect("localhost", 1883)
                client.loop_start()
                client.loop_stop()
                client.disconnect()

        def on_connect(self, client, rc):
            print("Client connected with result code: " + str(rc))
            # Publish a message when the client is connected (replace with your desired topic and message)
            client.publish(f"{self.owner.pz_id}_display_value", self.vacant_spaces)

    def __init__(self, jid: str, password: str, pz_id: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.pz_id = pz_id

    async def setup(self):
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)
