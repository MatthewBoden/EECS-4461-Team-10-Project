# EECS-4461-Team-10-Project
This is the final project for EECS 4461 for the Winter semester 2024/25  

## §A. Overview of the current implementation state.
### System Overview
- Agents: Two main types—AI vehicles (which have V2V communication) and human vehicles (which follow stochastic behaviour).
- Environment: A 7-lane, 60-length highway modelled using a grid-based approach (OrthogonalMooreGrid) to facilitate lane-based movement and interactions.
- Model Reporters: Data collection is a priority, with key metrics logged in `model_reporter` for empirical analysis.
- Phenomenon of Interest: The emergent behaviour of AI vehicles, particularly their V2V communication and collision avoidance mechanisms.
- Collision & Lane Detection: Real-time detection of collisions and lane changes, forming the basis of emergent behaviours.
- Scheduler & Spawning: Agents are dynamically spawned and activated via `shuffle_do("step")`, as Mesa deprecated formal schedulers.

### Agent Design
- `VehicleAgent` (Base Class): Governs movement logic and neighbour detection for both AI and human vehicles.
- `AIVehicle` Class: Implements V2V communication, using `left_sway_coefficient` and `right_sway_coefficient` to determine lane-change behaviour when detecting nearby AI vehicles.
- `HumanVehicle` Class: Lacks V2V communication and moves randomly, simulating human perception limitations and errors.

### Interaction Dynamics
- AI-to-AI: V2V signals are exchanged when AI vehicles are within a 3-cell distance, triggering avoidance behaviours.
- Collisions: AI-to-AI, AI-to-human, and human-to-human collisions are tracked, with AI interactions being the main focus.

### Data Collection & Visualization
Key metrics logged include:
- Agent counts (human & AI) to analyze variance effects.
- Collision data (AI-AI, human-human, AI-human) to evaluate V2V effectiveness.
- Step count for tracking emergent behaviours over time.
- Other data sources for key emergent behaviours.

### Preliminary Observations & Results 
Collision Behavior (non-emergent): AI-to-AI collisions were lower than human-to-human ones, confirming our hypothesis. Statistical analysis supports that V2V communication improves safety.
Protective Behavior (emergent): AI vehicles gravitated toward outer lanes, an emergent phenomenon likely driven by V2V interactions.
Ping-Pong Effect (emergent): A lone AI vehicle oscillated between two others in adjacent lanes, further reducing collisions.

Implications: These findings suggest AI lane usage patterns could inform real-world infrastructure, such as dedicated AI lanes.
Next Steps: We will investigate V2V parameters, particularly sway coefficients, to further understand these behaviors.

## §B. How to run the simulation
Ensure you have the latest version of Python (>= 3.11) installed. You can download it from the official Python website.

1. Create a Virtual Environment
    - Open VSCode and press Ctrl+Shift+P
    - Search for "Python: Create Virtual Environment" and follow the prompts
    - Search for "Python: Select Interpreter" and select the interpreter you installed

2. Install Dependencies
    - Run the following commands in your terminal:
    ```
    pip install -r requirements.txt
    ```

3. Run the Application
    - Run the following commands in your terminal:
    ```
    cd src
    ```
    ```
    solara run app.py
    ```

## §C. Limitations and planned improvements for the next phase.

Although we have made great progress and have uncovered emergent phenomena, we still plan on making improvements to the final version. We plan on visualizing collisions between agents, tweaking the left and right sway coefficients, conducting deeper explorations into emergent behaviour, and creating a malfunction rate for our V2V implementation to potentially uncover more unanticipated behaviour.
