import mesa
import random

class VehicleAgent(mesa.experimental.cell_space.CellAgent):
    def update_neighbors(self):
        """
        Look around and see who my neighbors are
        """
        self.neighborhood = self.cell.get_neighborhood(radius=self.vision) 

        self.neighbors = self.neighborhood.agents

        empty_neighbors = []
        for c in self.neighborhood:
            if c.coordinate[1] - self.cell.coordinate[1] == 1 and (abs(c.coordinate[0] - self.cell.coordinate[0]) == 1 or c.coordinate[0] - self.cell.coordinate[0] == 0): # checks y value to move forward
                empty_neighbors.append(c)
        self.empty_neighbors = empty_neighbors

class HumanVehicle(VehicleAgent):
    """
    A human driving a vehicle. Prone to error and poor decision making.

    Attributes:
        vision: number of cells in each direction that agent can inspect
    """

    def __init__(self, model, vision, is_middle):
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
        self.is_middle = is_middle
        
        # New attributes for collision detection
        self.detected_potential_collision = False
        self.avoided_collision = False

    def move(self):
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.successful_lane_changes += 1
            self.move_to(new_pos)

    def step(self):
        """
        Update potential lane changes and move to one of them.
        """
        self.update_neighbors()
        
        # Detect potential collision
        if self.detect_potential_collision():
            self.detected_potential_collision = True
            if self.can_avoid_collision():
                self.avoided_collision = True
        
        self.move()

    def detect_potential_collision(self):
        for neighbor in self.neighbors:
            if isinstance(neighbor, VehicleAgent):
                return True
        return False

    def can_avoid_collision(self):
        return len(self.empty_neighbors) > 0

class AIVehicle(VehicleAgent):
    """
    An AI self-driving vehicle. V2V enabled.

    Attributes:
        vision: number of cells in each direction that AI is able to inspect
    """

    def __init__(self, model, vision, is_middle, left_sway_coefficient, right_sway_coefficient, ai_malfunction_rate):
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
        self.is_middle = is_middle

        self.left_sway_coefficient = left_sway_coefficient
        self.right_sway_coefficient = right_sway_coefficient

        self.ai_malfunction_rate = ai_malfunction_rate
        
        # New attributes for collision detection
        self.detected_potential_collision = False
        self.avoided_collision = False
        

    def move(self):
        # V2V Phenomenon

        if self.model.movement and self.empty_neighbors:
            if random.random() * 100 < self.ai_malfunction_rate:
                # 90% chance of a random movement which may or may not lead to a collision
                if random.random() < 0.9: 
                    new_pos = random.choice(self.empty_neighbors)
                    #self.model.successful_lane_changes += 1
                # 10% chance to move aggressively which leads to almost a gurantee collision
                else:
                    if len(self.empty_neighbors) > 1:
                        new_pos = self.empty_neighbors[-1]
                        #self.model.successful_lane_changes += 1
                    else:
                        new_pos = self.empty_neighbors[0]
                    
                self.move_to(new_pos)
                return

        if self.model.movement and self.empty_neighbors:
            for neighbor in self.neighbors:
                cur_x = self.cell.coordinate[0]
                cur_y = self.cell.coordinate[1]
                neighbor_x = neighbor.cell.coordinate[0]
                neighbor_y = neighbor.cell.coordinate[1]
                if (cur_y == neighbor_y or neighbor_y - cur_y == 1) and neighbor.__class__ == AIVehicle: # agents in nearby rows
                    if neighbor_x > cur_x: # if AI neighbor is to the right of us
                        result = random.random() < self.left_sway_coefficient # the parameter to configure how often the V2V logic dictates to move left
                        if result:
                            new_pos = self.empty_neighbors[0] # change lanes to the left
                            #self.model.successful_lane_changes += 1
                        elif len(self.empty_neighbors) == 2:
                            new_pos = self.empty_neighbors[0] # stay in same lane because no space to the left
                        else:
                            new_pos = self.empty_neighbors[1] # stay in the same lane
                        self.move_to(new_pos)
                        return
                    elif neighbor_x < cur_x: # if AI neighbor is to the left of us
                        result = random.random() < self.right_sway_coefficient # the parameter to configure how often the V2V logic dictates to move right
                        if result and len(self.empty_neighbors) == 3:
                            new_pos = self.empty_neighbors[2] # change lanes to the right if not on edge
                            #self.model.successful_lane_changes += 1
                        else:
                            new_pos = self.empty_neighbors[1] # stay in the same lane
                        self.move_to(new_pos)
                        return

            new_pos = self.random.choice(self.empty_neighbors)
            self.move_to(new_pos)

    def step(self):
        """
        Update potential lane changes using V2V and move to one of them.
        """
        self.update_neighbors()
        
        # Detect potential collision
        if self.detect_potential_collision():
            self.detected_potential_collision = True
            if self.can_avoid_collision():
                self.avoided_collision = True

        if self.detect_potential_collision():
            self.detected_potential_collision = True        
        
        self.move()

    def detect_potential_collision(self):
        for neighbor in self.neighbors:
            if isinstance(neighbor, VehicleAgent):
                return True
        return False

    def can_avoid_collision(self):
        return len(self.empty_neighbors) > 0
