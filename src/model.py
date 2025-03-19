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
        height=60,
        ai_vision=3,
        human_vision=1,
        left_sway_coefficient=0.5,
        right_sway_coefficient=0.5,
        movement=True,
        max_iters=10000,
        seed=None,
        ai_malfunction_rate=0,
    ):
        super().__init__(seed=seed)

        # Model Params
        self.max_iters = max_iters
        self.movement = movement
        self.ai_vision = ai_vision
        self.human_vision = human_vision
        self.height = height
        self.width = width
        self.left_sway_coefficient = left_sway_coefficient
        self.right_sway_coefficient = right_sway_coefficient
        self.ai_malfunction_rate = ai_malfunction_rate

        self.grid = mesa.experimental.cell_space.OrthogonalMooreGrid(
            (width, height), capacity=10, torus=False, random=self.random
        )

        # Data Elements
        self.step_count = 0

        self.human_count = 1
        self.ai_count = 1

        self.ai_ai_collisions = 0
        self.human_human_collisions = 0
        self.ai_human_collisions = 0

        self.middle_ai_time_in_polar_lanes = 0
        self.middle_human_time_in_polar_lanes = 0

        self.middle_ai_polar_rate = 0
        self.middle_human_polar_rate = 0

        self.collided_cells = set()

        model_reporters = {
            "AI-AI Collisions": lambda m: m.ai_ai_collisions,
            "Human-Human Collisions": lambda m: m.human_human_collisions,
            "AI-Human Collisions": lambda m: m.ai_human_collisions,
            "AI Agents": lambda m: m.ai_count,
            "Human Agents": lambda m: m.human_count,
            "AI Agents in Polar Lanes": lambda m: m.middle_ai_polar_rate,
            "Human Agents in Polar Lanes": lambda m: m.middle_human_polar_rate
        }

        self.datacollector = mesa.DataCollector(model_reporters=model_reporters)
        self.datacollector.collect(self)

        # need to create initial vehicles when initializing system
        ai_vehicle = AIVehicle(self, vision=ai_vision, is_middle=False, left_sway_coefficient=self.left_sway_coefficient, right_sway_coefficient=self.right_sway_coefficient, ai_malfunction_rate=self.ai_malfunction_rate)
        human_vehicle = HumanVehicle(self, vision=human_vision, is_middle=True)

        for cell in self.grid.all_cells:
            if cell.coordinate == (1, 0):
                ai_vehicle.move_to(cell)
            if cell.coordinate == (5, 0):
                human_vehicle.move_to(cell)
        
        self.running = True
    
    def step(self):
        """
        Advance the model by one step and collect data.
        """
        self.agents.shuffle_do("step")

        self.collided_cells.clear()

        for cell in self.grid.all_cells:
            # Next 3 blocks are for the dynamic spawning of agents, random # and random types per row

            # [Optional] Spawn of random agent type in far left column
            first_spawn_result = random.random() < 0.5
            if first_spawn_result:
                if cell.coordinate == (0, 0) and cell.is_empty:
                    result = random.random() < 0.5
                    if result:
                        ai_vehicle = AIVehicle(self, vision=self.ai_vision, is_middle=False, left_sway_coefficient=self.left_sway_coefficient, right_sway_coefficient=self.right_sway_coefficient, ai_malfunction_rate=self.ai_malfunction_rate)
                        ai_vehicle.move_to(cell)
                        self.ai_count += 1
                    else:
                        human_vehicle = HumanVehicle(self, vision=self.human_vision, is_middle=False)
                        human_vehicle.move_to(cell) 
                        self.human_count += 1

            # [Optional] Spawn of random agent in far right column
            second_spawn_result = random.random() < 0.5
            if second_spawn_result:
                if cell.coordinate == (6, 0) and cell.is_empty:
                    result = random.random() < 0.5
                    if result:
                        ai_vehicle = AIVehicle(self, vision=self.ai_vision, is_middle=False, left_sway_coefficient=self.left_sway_coefficient, right_sway_coefficient=self.right_sway_coefficient, ai_malfunction_rate=self.ai_malfunction_rate)
                        ai_vehicle.move_to(cell)
                        self.ai_count += 1
                    else:
                        human_vehicle = HumanVehicle(self, vision=self.human_vision, is_middle=False)
                        human_vehicle.move_to(cell) 
                        self.human_count += 1
                
            # [Mandatory] Spawn of random agent in middle column
            if cell.coordinate == (3, 0) and cell.is_empty:
                result = random.random() < 0.5
                if result:
                    ai_vehicle = AIVehicle(self, vision=self.ai_vision, is_middle=True, left_sway_coefficient=self.left_sway_coefficient, right_sway_coefficient=self.right_sway_coefficient, ai_malfunction_rate=self.ai_malfunction_rate)
                    ai_vehicle.move_to(cell)
                    self.ai_count += 1
                    
                else:
                    human_vehicle = HumanVehicle(self, vision=self.human_vision, is_middle=True)
                    human_vehicle.move_to(cell) 
                    self.human_count += 1

            # Removal of agents when they reach the end of the grid 
            if (cell.coordinate[1] == self.height - 1) and cell.is_empty == False:
                cell.remove_agent(cell.agents[0])
                continue
            
            # collision between two agents
            if (len(cell.agents) == 2):
                self.collided_cells.add(cell.coordinate)
    
                agent1 = cell.agents[0]
                agent2 = cell.agents[1]

                if isinstance(agent1, AIVehicle) and isinstance(agent2, AIVehicle):
                    self.ai_ai_collisions += 1
                elif isinstance(agent1, HumanVehicle) and isinstance(agent2, HumanVehicle):
                    self.human_human_collisions += 1
                else:
                    self.ai_human_collisions += 1
                    
            # collision between three agents
            if len(cell.agents) == 3:
                self.collided_cells.add(cell.coordinate)

                agent1 = cell.agents[0]
                agent2 = cell.agents[1]
                agent3 = cell.agents[2]

                temp_ai_count = sum(isinstance(agent, AIVehicle) for agent in (agent1, agent2, agent3))
                temp_human_count = 3 - temp_ai_count
                
                if temp_ai_count == 3:
                    self.ai_ai_collisions += 2
                elif temp_human_count == 3:
                    self.human_human_collisions += 2
                elif temp_ai_count == 2:
                    self.ai_ai_collisions += 1
                    self.ai_human_collisions += 1
                elif temp_human_count == 2:
                    self.human_human_collisions += 1
                    self.ai_human_collisions += 1    

            # check agents that made it to end lanes
            if cell.coordinate[0] == 0 or cell.coordinate[0] == self.width-1: 
                if not cell.is_empty:
                    for agent in cell.agents:
                        if agent.__class__ == AIVehicle and agent.is_middle:
                            self.middle_ai_time_in_polar_lanes += 1
                        if agent.__class__ == HumanVehicle and agent.is_middle:
                            self.middle_human_time_in_polar_lanes += 1

        self.step_count += 1

        self.middle_ai_polar_rate = self.middle_ai_time_in_polar_lanes / self.step_count
        self.middle_human_polar_rate = self.middle_human_time_in_polar_lanes / self.step_count
        
        self.datacollector.collect(self)

        if self.steps > self.max_iters:
            self.running = False
