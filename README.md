# EECS-4461-Team-10-Project
This is the final project for EECS 4461 for the Winter semester 2024/25  

## Interim Prototype Overview
### **Current Implementation State**
The current implementation of our simulation models **Vehicle-to-Vehicle (V2V) communication** among AI-driven self-driving cars. This allows vehicles to share information about their surroundings, road conditions, and movement analytics in real time. 

Using **Agent-Based Modeling (ABM)**, our prototype simulates AI-to-AI, AI-to-human, and human-to-human interactions within a media ecosystem. The goal is to analyze emergent behaviors and unexpected consequences in self-driving vehicle networks. 

The prototype features:
- **Realistic AI vehicle interactions** via omnidirectional radio signals
- **Machine learning optimization** to improve V2V communication
- **Simulation of thousands of vehicles** interacting in a complex system
- **Collision tracking and behavioral analysis**

This prototype is a crucial step toward identifying potential risks and benefits of V2V communication in real-world traffic systems.

## Getting Started
Ensure you have the latest version of Python (>= 3.11) installed. You can download it from the official Python website.

1. Create a Virtual Environment
    - Open VSCode and press Ctrl+Shift+P
    - Search for "Python: Create Virtual Environment" and follow the prompts
    - Search for "Python: Select Interpreter" and select the interpreter you installed

2. Install Dependencies
    - Run the following commands in your terminal:

    ```
    pip install -U --pre mesa[all]
    pip uninstall -y ipyvue ipyvuetify
    pip install ipyvue==1.11.2
    pip install ipyvuetify==1.10.0
    ```

3. Run the Application
    - Navigate to the an example directly like `boid` or `epstein`
    - Start the application `solara run app.py`