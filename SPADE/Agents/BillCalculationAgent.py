from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class BillCalculationAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)

    class BillCalculationAgent(CyclicBehaviour):

        async def on_start(self):
            self.isVacant = False

        async def run(self):
            print("Current Sensor Value: {}".format(sensorvalue))
            self.counter += 1
            if self.counter > 30:
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    async def setup(self):
        b = self.MyBehav()
        self.add_behaviour(b)
