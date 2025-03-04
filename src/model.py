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
        ai_vision=3,
        human_vision=1,
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

        self.ai_ai_collisions = 0
        self.human_human_collisions = 0
        self.ai_human_collisions = 0


        model_reporters = {
            "AI-AI Collisions": lambda m: m.ai_ai_collisions,
            "Human-Human Collisions": lambda m: m.human_human_collisions,
            "AI-Human Collisions": lambda m: m.ai_human_collisions,
        }

        self.datacollector = mesa.DataCollector(model_reporters=model_reporters)
        self.datacollector.collect(self)


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

                agent1 = cell.agents[0]
                agent2 = cell.agents[1]

                if isinstance(agent1, AIVehicle) and isinstance(agent2, AIVehicle):
                    self.ai_ai_collisions += 1
                elif isinstance(agent1, HumanVehicle) and isinstance(agent2, HumanVehicle):
                    self.human_human_collisions += 1
                else:
                    self.ai_human_collisions += 1
                
                self.datacollector.collect(self)


        if self.steps > self.max_iters:
            self.running = False


