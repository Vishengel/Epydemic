import config, time
import numpy as np

from mesa import Agent

class PyDemicAgent(Agent):
    def __init__(self, unique_id, model, pos, speed=config.agent_speed, heading=None, infected=False, cured=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        self.radius = config.agent_radius
        self.infected = infected
        self.cured = cured

        if heading is not None:
            self.heading = heading
        else:
            self.heading = np.random.random(2) * 2 - 1
            self.heading /= np.linalg.norm(self.heading)

        if self.infected:
            self.time_infected = time.time()

    def step(self):
        # Check if the agent collides with another
        colliding_agents = self.check_collision()
        # Handle collision (if any)
        if len(colliding_agents) > 0:
            for colliding_agent in colliding_agents:
                # Calculate new headings for both agents
                self.apply_collision(colliding_agent)
                # Check if an agent gets infected, apply infection if necessary
                self.apply_infection(colliding_agent)

        if self.infected:
            if time.time() - self.time_infected > config.recovery_time:
                self.infected = False
                self.cured = True

        new_pos = np.array(self.pos) + self.heading * self.speed
        new_x, new_y = new_pos
        self.model.space.move_agent(self, (new_x, new_y))

    def check_collision(self):
        colliding_agents = []
        for agent in self.model.schedule.agents:
            if self.unique_id == agent.unique_id:
                continue

            if ((self.pos[0] - agent.pos[0])**2 + (self.pos[1] - agent.pos[1])**2) <= (self.radius + agent.radius)**2:
                colliding_agents.append(agent)

        return colliding_agents

    def apply_collision(self, agent):
        tangent_x = abs(agent.pos[1] - self.pos[1])
        tangent_y = -1*abs(agent.pos[0] - self.pos[0])
        tangent_vector = np.array([tangent_x, tangent_y])
        tangent_vector /= np.linalg.norm(tangent_vector)

        relative_velocity = np.array([self.heading[0] - agent.heading[0], self.heading[1] - agent.heading[1]])
        length = np.dot(relative_velocity, tangent_vector)
        velocity_comp_on_tangent = np.multiply(tangent_vector, length)
        velocity_comp_perp = relative_velocity - velocity_comp_on_tangent

        self.heading[0] -= velocity_comp_perp[0]
        self.heading[1] -= velocity_comp_perp[1]
        self.heading /= np.linalg.norm(self.heading)

        agent.heading[0] += velocity_comp_perp[0]
        agent.heading[1] += velocity_comp_perp[1]
        agent.heading /= np.linalg.norm(agent.heading)

    def apply_infection(self, colliding_agent):
        # If the other agent is infected, and this agent has not been infected yet: make agent infected
        if colliding_agent.infected and not (self.infected or self.cured):
            self.infected = True
            self.time_infected = time.time()
        # And vice versa for the other agent
        if self.infected and not (colliding_agent.infected or colliding_agent.cured):
            colliding_agent.infected = True
            colliding_agent.time_infected = time.time()