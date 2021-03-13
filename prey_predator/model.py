"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from typing import Union
from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed
import random


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """
    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    grass_presence_probability = 1.0

    moore = True

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
            self,
            height=20,
            width=20,
            initial_sheep=100,
            initial_wolves=50,
            sheep_reproduce=0.04,
            wolf_reproduce=0.05,
            wolf_gain_from_food=20,
            grass=False,
            grass_regrowth_time=30,
            sheep_gain_from_food=4,
            initial_energy=10,
            moore=True,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.initial_energy = initial_energy

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.counter = 0
        self.moore = moore
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for _ in range(initial_sheep):
            initial_position = (random.randint(0, height - 1), random.randint(0, width - 1))

            # Incrementing counter
            self.counter += 1

            # Creating sheep agent
            sheep_agent = Sheep(self.counter, initial_position, self, moore, initial_energy)

            # Adding sheep agent
            self.schedule.add(sheep_agent)

            # Placing agent
            self.grid.place_agent(sheep_agent, initial_position)

        # Create wolves
        for _ in range(initial_wolves):
            # Defining initial position
            initial_position = (random.randint(0, height - 1), random.randint(0, width - 1))

            # Incrementing counter
            self.counter += 1

            # Creating wolf agent
            wolf_agent = Wolf(self.counter, initial_position, self, moore, initial_energy)

            # Adding agent
            self.schedule.add(wolf_agent)

            # Placing agent
            self.grid.place_agent(wolf_agent, initial_position)

        # Create grass patches
        for grid_height in range(height):
            for grid_width in range(width):
                # Incrementing counter
                self.counter += 1

                # Creating GrassPatch agent
                grass_patch_agent = GrassPatch(
                    self.counter,
                    self,
                    True,
                    self.grass_regrowth_time
                )

                # Adding agent
                self.schedule.add(grass_patch_agent)

                # Placing agent
                self.grid.place_agent(grass_patch_agent, (grid_height, grid_width))

    def get_agents_at_position(self, position: tuple):
        """
        Returns all the agents located at a specific location
        """
        return self.grid.get_cell_list_contents([position])

    def get_grass_patch_to_eat_at_position(self, position: tuple) -> Union[GrassPatch, None]:
        """
        This function returns a GrassPatch agent if and only if this agent is eatable
        """
        grass_patch = None
        agents = self.get_agents_at_position(position)

        for agent in agents:
            if type(agent) == GrassPatch:
                grass_patch = agent
                break

        return grass_patch if grass_patch.is_eatable() else None

    def get_sheep_to_eat_at_position(self, position: tuple) -> Union[Sheep, None]:
        """
        This function returns a sheep agent to be eaten by a wolf agent if the wolf agents calling this function shares
        its tile with a sheep agent. If there are several sheep agents on the same tile, one of them will be chosen randomly.
        """
        sheep_agent = None
        agents = self.get_agents_at_position(position)

        for agent in agents:
            if type(agent) == Sheep:
                sheep_agent = agent
                break

        return sheep_agent

    def add_new_agent(self, agent_type: str, pos: tuple):
        agent = None

        # Increasing counter
        self.counter += 1

        if agent_type == Wolf:
            agent = Wolf(self.counter, pos, self, self.moore, self.initial_energy)
        elif agent_type == Sheep:
            agent = Sheep(self.counter, pos, self, self.moore, self.initial_energy)

        # Adding agent in schedule's agents array
        self.schedule.add(agent)

        # Placing agent in the grid
        self.grid.place_agent(agent, pos)

    def remove_agent(self, agent: Agent):
        """
        This function is to be called when an agent dies
        """
        # Removing agent from the grid
        self.grid.remove_agent(agent)

        # Removing agent from schedule
        self.schedule.remove(agent)

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):
        # Iterating
        for step in range(step_count):
            self.schedule.step()

            # Collect data
            self.datacollector.collect()
