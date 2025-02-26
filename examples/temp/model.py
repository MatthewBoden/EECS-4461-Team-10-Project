import mesa
from agent import (
    AIVehicle,
    HumanVehicle,
)


class HighwayV2VModel(mesa.Model):
    """
    Model 1 from "Modeling civil violence: An agent-based computational
    approach," by Joshua Epstein.
    http://www.pnas.org/content/99/suppl_3/7243.full

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
            (width, height), capacity=2, torus=False, random=self.random
        )

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

        ai_vehicle = AIVehicle(self, vision=vision)
        human_vehicle = HumanVehicle(self, vision=vision)

        for cell in self.grid.all_cells:
            # the beginning
            if cell.coordinate == (1, 0) and cell.empty:
                ai_vehicle.move_to(cell) # MESA ERROR IS THIS, weird bug.
            if cell.coordinate == (5, 0) and cell.empty:
                human_vehicle.move_to(cell) 

            # and the end
            if (cell.coordinate[1] == 69) and cell.empty == False:
                cell.remove_agent(cell.agents[0])

            # collision
            if (len(cell.agents) == 2):
                print("Collision!")
                # add collision logic


        if self.steps > self.max_iters:
            self.running = False