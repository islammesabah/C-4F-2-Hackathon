import random


class Agent:
    def select_action(self, state, conn=None, vehicle_ids=None):
        return random.randint(0, 1)
