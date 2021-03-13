from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy: int = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def is_eaten(self):
        """
        This function is to be called by a wolf agent so as to remove the sheep agent from the environment
        """
        self.model.remove_agent(self)

    def random_move(self):
        super().random_move()

        # Decreasing agent's energy if grass is eatable
        if self.model.grass:
            self.energy -= 1

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()

        # Checking if the agent is dead
        if self.energy == 0:
            self.model.remove_agent(self)
            return

        # Checking if the sheep agent can gain energy by eating grass patch
        if self.model.grass:
            # Checking if there is an eatable grass patch at the current position
            grass_patch = self.model.get_grass_patch_to_eat_at_position(self.pos)

            if grass_patch:
                # Eating grass
                grass_patch.is_eaten()

                # Increasing energy
                self.energy += self.model.sheep_gain_from_food

        # Checking if we can add a new sheep agent in the environment
        if random.random() <= self.model.sheep_reproduce:
            self.reproduce()


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def random_move(self):
        super().random_move()

        # Decreasing agent's energy
        self.energy -= 1

    def step(self):
        self.random_move()

        # Checking if the agent is dead
        if self.energy == 0:
            self.model.remove_agent(self)
            return

        # Checking if there is a sheep agent to eat at the current position
        sheep = self.model.get_sheep_to_eat_at_position(self.pos)

        if sheep:
            sheep.is_eaten()

            # Increasing agent's energy
            self.energy += self.model.wolf_gain_from_food

        # Checking if we could add a new wolf agent in the environment
        if random.random() <= self.model.wolf_reproduce:
            self.reproduce()


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """
    grown: bool
    countdown: int
    steps_before_full_regrowth: int

    def __init__(self, unique_id, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # Specifying if the patch of grass should be displayed in the environment
        self.grown = fully_grown

        # Setting growth rate
        self.countdown = countdown

        # Setting the number of steps before full regrowth
        self.steps_before_full_regrowth = 0 if self.grown else self.countdown

    def is_eaten(self):
        """
        This function will be called by a sheep agent after it has eaten this patch of grass
        """
        self.grown = False
        self.steps_before_full_regrowth = self.countdown

    def is_eatable(self):
        """
        Returns a boolean to indicate whether or not this grass patch can be eaten
        """
        return self.grown

    def step(self):
        # Checking if the we should decrease steps_before_fully_regrowth
        if not self.grown:
            # Decreasing value of steps_before_fully_regrowth
            self.steps_before_full_regrowth -= 1

            # Checking whether the patch of grass is fully grown or not
            if self.steps_before_full_regrowth == 0:
                self.grown = True
