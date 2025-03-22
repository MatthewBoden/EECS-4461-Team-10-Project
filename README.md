# EECS-4461-Team-10-Project
This is the final project for EECS 4461 for the Winter semester 2024/25  

## §A. Overview of the phenomenon

The research examines Vehicle-to-Vehicle (V2V) communication between self-driving cars, conceptualized as a complex media ecosystem. V2V enables AI vehicles to exchange information about road conditions and surroundings through omnidirectional radio signals. The researchers developed agent-based models (ABM) to understand how these interactions affect road safety and to identify emergent behaviors.
Key aspects of the phenomenon include:

### Media Ecosystem Framework
The simulation work frames roads as a media ecosystem where AI vehicles (biotic elements) interact with human-driven vehicles and infrastructure (abiotic elements). This ecosystem follows a trophic structure with car manufacturers as primary producers and various stakeholders (users, reviewers, analysts, and regulators) as consumers.

### Problem Statement
As AI self-driving vehicles become more prevalent globally, understanding potential unforeseen emergent behaviors in V2V systems is crucial for ensuring road safety. The research aims to identify these behaviors through simulation to improve system safety.

### Methodology
Agent-Based Modeling was selected due to its suitability for studying complex micro-level interactions. The simulation used a 7×60 grid representing a highway section, with agents (AI and human vehicles) spawning at the bottom and moving upward. The model tracked various metrics including collision rates and lane positioning.

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
Key metrics logged include but are not limited to:
- Agent counts (human & AI) to analyze variance effects.
- Collision data (AI-AI, human-human, AI-human) to evaluate V2V effectiveness.
- Step count for tracking emergent behaviours over time.
- Other data sources for key emergent behaviours.

## §B. How to run the simulation
Ensure you have the latest version of Python (>= 3.11) installed. You can download it from the official Python website.

1. Install Dependencies
    - Run the following commands in your terminal:
    ```
    pip install -r requirements.txt
    ```

2. Run the Application
    - Run the following commands in your terminal:
    ```
    cd src
    ```
    ```
    solara run app.py
    ```

## §C. Key findings or observations

### Collision Behaviour
AI-to-AI collisions were consistently lower than human-to-human collisions, supporting the effectiveness of Vehicle-to-Vehicle (V2V) communication in reducing accidents.

Across five simulation runs at step 5000, AI-to-AI collisions averaged 4,411 (±160.46), while human-to-human collisions averaged 12,318 (±284.60).

This suggests that V2V meets its baseline goal of improving safety through AI coordination.

### Emergent Protective Behaviour
AI self-driving vehicles displayed an unexpected protective behaviour, tending toward the leftmost and rightmost lanes over time.

Initially, human-driven vehicles exhibited a stronger preference for polar lanes, but by step 1000, AI vehicles surpassed them (mean 9.72 AI vs. 5.55 human).

This emergent phenomenon appears to be a direct consequence of V2V interactions, leading to a self-organized safety mechanism.

Parameter tuning revealed that setting sway coefficients to 0.1 led to an equal distribution between AI and human vehicles in polar lanes, a key insight for V2V system design.

### Emergent Ping-Pong Effect
When three AI agents occupied the same lane, the middle agent exhibited a "ping-pong" effect, oscillating between two AI vehicles in the polar lanes.

This effect likely contributed to lower AI-to-AI collision rates, reinforcing the role of V2V in collision avoidance.

The discovery suggests that future AI-driven systems should regulate V2V signal handling to prevent excessive lateral movement.

### Implications for Future Research
The protective behaviour may have real-world parallels, such as AI-dedicated lanes similar to High Occupancy Vehicle (HOV) lanes in Ontario. However, AI should not always assume polar lanes are safest.

The ping-pong effect highlights a need for machine learning-based decision-making in future self-driving cars to handle multiple V2V signals simultaneously.

Future V2V research should explore how AI vehicles distribute themselves in dynamic traffic environments and whether emergent safety behaviours align with real-world traffic patterns.

### Conclusion: Unexpected Behaviours and Emergent Dynamics
The protective behaviour and ping-pong effect emerged organically from V2V interactions rather than being explicitly coded.

These findings reinforce that complex AI systems develop higher-level patterns that cannot always be predicted from their base logic.

Further tuning of V2V parameters could refine AI driving strategies to ensure adaptability and robustness in mixed human-AI traffic systems.