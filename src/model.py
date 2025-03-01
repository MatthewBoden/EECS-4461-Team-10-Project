import mesa
import random
from agent import (
    AIVehicle,
    HumanVehicle,
)


class HighwayV2VModel(mesa.Model):
    """
    Model that illustrates AI-to-AI interactions between vehicles on a road grid.

    Args:
        height: grid height
        width: grid width
        ai_vision: vision range of AI vehicle
        human_vision: vision range of human vehicle
        movement: binary, whether agents try to move at step end
        max_iters: model may not have a natural stopping point, so we set a
            max.
    """

    def __init__(
        self,
        width=7,
        height=70,
        ai_vision=1,
        human_vision=0,
        movement=True,
        max_iters=1000,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.max_iters = max_iters
        self.movement = movement

        self.grid = mesa.experimental.cell_space.OrthogonalMooreGrid(
            (width, height), capacity=10, torus=False, random=self.random
        )

        # need to create initial vehicle to initialize system
        vehicle = AIVehicle(self, vision=ai_vision)
        for cell in self.grid.all_cells:
            if cell.coordinate == (3, 0):
                vehicle.move_to(cell)

        self.running = True
    
    def step(self):
        """
        Advance the model by one step and collect data.
        """
        self.agents.shuffle_do("step")
        vision = 1

        for cell in self.grid.all_cells:
            # Next 3 blocks are for the dynamic spawning of agents, random # and random types per row

            # [Mandatory] Spawn of random agent type in middle column
            if cell.coordinate == (0, 0) and cell.empty:
                result = random.random() < 0.5
                if result:
                    ai_vehicle = AIVehicle(self, vision=vision)
                    ai_vehicle.move_to(cell)
                else:
                    human_vehicle = HumanVehicle(self, vision=vision)
                    human_vehicle.move_to(cell) 

            # [Mandatory] Spawn of random agent type in middle column
            if cell.coordinate == (6, 0) and cell.empty:
                result = random.random() < 0.5
                if result:
                    ai_vehicle = AIVehicle(self, vision=vision)
                    ai_vehicle.move_to(cell)
                else:
                    human_vehicle = HumanVehicle(self, vision=vision)
                    human_vehicle.move_to(cell) 

            # [Optional] Spawn of random agent type in middle column
            third_spawn_result = random.random() < 0.5
            if third_spawn_result:
                if cell.coordinate == (3, 0) and cell.empty:
                    result = random.random() < 0.5
                    if result:
                        ai_vehicle = AIVehicle(self, vision=vision)
                        ai_vehicle.move_to(cell)
                    else:
                        human_vehicle = HumanVehicle(self, vision=vision)
                        human_vehicle.move_to(cell) 

            # Removal of agents when they reach the end of the grid 
            if (cell.coordinate[1] == 69) and cell.empty == False:
                cell.remove_agent(cell.agents[0])
            
            if (len(cell.agents) == 2):
                print("Collision!")
                for agent in cell.agents:
                    print(agent)
                print(cell.coordinate)


        if self.steps > self.max_iters:
            self.running = False


