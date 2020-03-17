import random

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from agent import PyDemicAgent

class PyDemicModel(Model):
    def __init__(self, n_agents, width=500, height=500):
        self.n_agents = n_agents
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.make_agents()
        self.running = True

    def step(self):
        self.schedule.step()

    def make_agents(self):
        for idx in range(self.n_agents):
            x_pos = random.random() * self.space.x_max
            y_pos = random.random() * self.space.y_max
            pos = (x_pos, y_pos)

            if idx == 0:
                agent = PyDemicAgent(idx, self, pos, infected=True)
            else:
                agent = PyDemicAgent(idx, self, pos, infected=False)

            self.space.place_agent(agent, pos)
            self.schedule.add(agent)
