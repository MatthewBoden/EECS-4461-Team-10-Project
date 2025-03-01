import mesa

class VehicleAgent(mesa.experimental.cell_space.CellAgent):
    def update_neighbors(self):
        """
        Look around and see who my neighbors are
        """

        # phenomenon will be: AI cars can detect if vehicle is AI (V2V), if it isnt (human) it will move away from it, expecting the human to be reckless
        # if it is V2V, it wouldnt avoid it, both go straight line. Maybe if AI car is next to another AI car, they go straight line
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision)

        # doing this to get the cells ahead
        self.forward_cells = []
        current_y = self.cell.coordinate[1]
        current_x = self.cell.coordinate[0]
        
        for c in self.neighborhood:
            # Only consider cells ahead within agent's vision range
            cell_distance = c.coordinate[1] - current_y
            if 0 < cell_distance <= self.vision and abs(c.coordinate[0] - current_x) <= 1:
                self.forward_cells.append(c)

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
    
    def move(self):
        """
        Humans move based on limited vision range.
        They can only see and react to immediate surroundings.
        """
        if not self.model.movement or not self.forward_cells:
            return


        error_chance = 0.25
        
        # if human makes a mistake (25% chance) then we move forward to any free cell meaning we can get a collision
        if self.random.random() < error_chance:
            new_move = self.random.choice(self.forward_cells)
            self.move_to(new_move)
            return
            
        # otherwise we cosnider empty cells
        empty_cells = [cell for cell in self.forward_cells if len(cell.agents) == 0]
        if empty_cells:
            new_move = self.random.choice(empty_cells)
            self.move_to(new_move)

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
    
    def move(self):
        """
        AI vehicles use extended vision range and V2V communication
        to make smarter moves and avoid collisions
        """

        if not self.model.movement or not self.forward_cells:
            return
        
        # Chance of a system failure for AI cars
        error_chance = 0.06
        
        # if there is a system failure then we just move forward to any free cell meaning we can get a collision
        if self.random.random() < error_chance:
            new_pos = self.random.choice(self.forward_cells)
            self.move_to(new_pos)
            return
            
        # if there is no system failure then we make a safe move by checking empty cells
        current_x = self.cell.coordinate[0]
        empty_cells = [cell for cell in self.forward_cells if len(cell.agents) == 0]
        
        if empty_cells:
            # there is a 2x chance to move to a cell in the same lane cuz it is safer 
            weights = [2 if cell.coordinate[0] == current_x else 1 for cell in empty_cells]
            new_pos = self.random.choices(empty_cells, weights=weights, k=1)[0]
            self.move_to(new_pos)

    def step(self):
        """
        Update potential lane changes using V2V and move to one of them.
        """
        self.update_neighbors()
        self.move()
