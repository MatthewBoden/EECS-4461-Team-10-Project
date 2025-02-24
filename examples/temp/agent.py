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
        # Find empty cells (cells with no other agents)
        empty_cells = [cell for cell in self.empty_neighbors if not cell.agents]

        if empty_cells:
            self.move_to(self.random.choice(empty_cells))



class HumanVehicle(VehicleAgent):
    """
    A member of the general population, may or may not be in active rebellion.
    Summary of rule: If grievance - risk > threshold, rebel.

    Attributes:
        hardship: Agent's 'perceived hardship (i.e., physical or economic
            privation).' Exogenous, drawn from U(0,1).
        regime_legitimacy: Agent's perception of regime legitimacy, equal
            across agents.  Exogenous.
        risk_aversion: Exogenous, drawn from U(0,1).
        threshold: if (grievance - (risk_aversion * arrest_probability)) >
            threshold, go/remain Active
        vision: number of cells in each direction (N, S, E and W) that agent
            can inspect
        condition: Can be "Quiescent" or "Active;" deterministic function of
            greivance, perceived risk, and
        grievance: deterministic function of hardship and regime_legitimacy;
            how aggrieved is agent at the regime?
        arrest_probability: agent's assessment of arrest probability, given
            rebellion
    """

    def __init__(self, model, vision):
        """
        Create a new Citizen.
        Args:
            model: the model to which the agent belongs
            hardship: Agent's 'perceived hardship (i.e., physical or economic
                privation).' Exogenous, drawn from U(0,1).
            regime_legitimacy: Agent's perception of regime legitimacy, equal
                across agents.  Exogenous.
            risk_aversion: Exogenous, drawn from U(0,1).
            threshold: if (grievance - (risk_aversion * arrest_probability)) >
                threshold, go/remain Active
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
            model: model instance
        """
        super().__init__(model)
        self.vision = vision
        self.neighborhood = []
        self.neighbors = []
        self.empty_neighbors = []

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
        self.update_neighbors()
        # self.update_estimated_arrest_probability()

        # net_risk = self.risk_aversion * self.arrest_probability
        # if (self.grievance - net_risk) > self.threshold:
        #     self.state = CitizenState.ACTIVE
        # else:
        #     self.state = CitizenState.QUIET

        self.move()

    # def update_estimated_arrest_probability(self):
    #     """
    #     Based on the ratio of cops to actives in my neighborhood, estimate the
    #     p(Arrest | I go active).
    #     """
    #     cops_in_vision = 0
    #     actives_in_vision = 1  # citizen counts herself
    #     for neighbor in self.neighbors:
    #         if isinstance(neighbor, Cop):
    #             cops_in_vision += 1
    #         elif neighbor.state == CitizenState.ACTIVE:
    #             actives_in_vision += 1

    #     # there is a body of literature on this equation
    #     # the round is not in the pnas paper but without it, its impossible to replicate
    #     # the dynamics shown there.
    #     self.arrest_probability = 1 - math.exp(
    #         -1 * self.arrest_prob_constant * round(cops_in_vision / actives_in_vision)
    #     )


class AIVehicle(VehicleAgent):
    """
    A cop for life.  No defection.
    Summary of rule: Inspect local vision and arrest a random active agent.

    Attributes:
        unique_id: unique int
        x, y: Grid coordinates
        vision: number of cells in each direction (N, S, E and W) that cop is
            able to inspect
    """

    def __init__(self, model, vision):
        """
        Create a new Cop.
        Args:
            x, y: Grid coordinates
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
            model: model instance
        """
        super().__init__(model)
        self.vision = vision
        self.neighborhood = []
        self.neighbors = []
        self.empty_neighbors = []

    def step(self):
        """
        Inspect local vision and arrest a random active agent. Move if
        applicable.
        """
        self.update_neighbors()
        # active_neighbors = []
        # for agent in self.neighbors:
        #     if isinstance(agent, Citizen) and agent.state == CitizenState.ACTIVE:
        #         active_neighbors.append(agent)
        # if active_neighbors:
        #     arrestee = self.random.choice(active_neighbors)
        #     arrestee.jail_sentence = self.random.randint(0, self.max_jail_term)
        #     arrestee.state = CitizenState.ARRESTED

        self.move()
