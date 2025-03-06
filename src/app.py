from agent import (
    AIVehicle,
    HumanVehicle,
)
from model import HighwayV2VModel
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def portrayal(agent):
    if agent is None:
        return

    portrayal = { 
        "size": 75, 
        "marker": "^"
    }

    if isinstance(agent, AIVehicle):
        portrayal["color"] = "#AA4A44"
    elif isinstance(agent, HumanVehicle):
        portrayal["color"] = "#808080"

    return portrayal

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(15, 15)

def customize_plot_1(ax):
    ax.set_title("Collisions Over Time: AI-AI Vs Human-Human Vs AI-Human")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Number of Collisions")
    ax.legend(loc="upper left")
    ax.get_figure().set_size_inches(8, 4)

def customize_plot_2(ax):
    ax.set_title("Average Count of Middle Spawning Agents in Polar Lanes Over Time")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Average Number of Agents per Step")
    ax.legend(loc="upper left")
    ax.get_figure().set_size_inches(8, 4)

def customize_plot_3(ax):
    ax.set_title("Total Agent Count Over Time")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Number of Agents")
    ax.legend(loc="upper left")
    ax.get_figure().set_size_inches(8, 4)

def space_filler_plot(ax):
    ax.get_figure().set_visible(False)

collision_chart = make_plot_component(
    {
        "AI-AI Collisions": "#AA4A44",
        "Human-Human Collisions": "#808080",
        "AI-Human Collisions": "#000000"     
    },
    post_process=customize_plot_1,
    backend="matplotlib"
)

polar_lane_average = make_plot_component(
    {
        "AI Agents in Polar Lanes": "#AA4A44",
        "Human Agents in Polar Lanes": "#808080",
    },
    post_process=customize_plot_2,
    backend="matplotlib"
)

agent_count_chart = make_plot_component(
    {
        "AI Agents": "#AA4A44",
        "Human Agents": "#808080",
    },
    post_process=customize_plot_3,
    backend="matplotlib"
)

space_fill = make_plot_component(
    {},
    post_process=space_filler_plot,
)

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "left_sway_coefficient": Slider("V2V Left Sway Coefficient", 0.5, 0.0, 1, 0.01),
    "right_sway_coefficient": Slider("V2V Right Sway Coefficient", 0.5, 0.0, 1, 0.01),
}

epstein_model = HighwayV2VModel()

space_component = make_space_component(
    portrayal, post_process=post_process, draw_grid=True
)

page = SolaraViz(
    epstein_model,
    components=[space_component, agent_count_chart, space_fill, polar_lane_average, space_fill, collision_chart],
    model_params=model_params,
    name="Highway V2V Model",
)
page