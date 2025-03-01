import mesa

class VehicleAgent(mesa.experimental.cell_space.CellAgent):
    def update_neighbors(self):
        """
        Look around and see who my neighbors are
        """

        # phenomenon will be: AI cars can detect if vehicle is AI (V2V), if it isnt (human) it will move away from it, expecting the human to be reckless
        # if it is V2V, it wouldnt avoid it, both go straight line. Maybe if AI car is next to another AI car, they go straight line
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision) 

        self.neighbors = self.neighborhood.agents

        empty_neighbors = []
        for c in self.neighborhood:
            if c.coordinate[1] > self.cell.coordinate[1]: # checks y value to move forward
                empty_neighbors.append(c)
        self.empty_neighbors = empty_neighbors

    def move(self):
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.move_to(new_pos)


class HumanVehicle(VehicleAgent):
    """
    A human driving a vehicle. Prone to error and poor decision making.

    Attributes:
        vision: number of cells in each direction that agent can inspect
    """

    def __init__(self, model, vision):
        """
        Create a new HumanVehicle.
        Args:
            model: the model to which the agent belongs
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
        """
        super().__init__(model)
        self.vision = vision
        self.neighborhood = []
        self.neighbors = []
        self.empty_neighbors = []

    def step(self):
        """
        Update potential lane changes and move to one of them.
        """
        self.update_neighbors()
        self.move()


class AIVehicle(VehicleAgent):
    """
    An AI self-driving vehicle. V2V enabled.

    Attributes:
        vision: number of cells in each direction that AI is able to inspect
    """

    def __init__(self, model, vision):
        """
        Create a new AIVehicle.
        Args:
            model: the model to which the agent belongs
            vision: number of cells in each direction that
                agent can inspect. Exogenous.
        """
        super().__init__(model)
        self.vision = vision
        self.neighborhood = []
        self.neighbors = []
        self.empty_neighbors = []

    def step(self):
        """
        Update potential lane changes using V2V and move to one of them.
        """
        self.update_neighbors()
        self.move()
