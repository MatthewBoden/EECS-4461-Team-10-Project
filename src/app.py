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
        "size": 50, 
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

def customize_plot(ax):
    ax.set_title("Accidents Over Time: AI-AI Vs Human-Human Vs AI-Human")
    ax.set_xlabel("Number of Steps")
    ax.set_ylabel("Number of Accidents")
    ax.grid(True)
    ax.legend(loc="upper left")

collision_chart = make_plot_component(
    {
        "AI-AI Collisions": "#AA4A44",
        "Human-Human Collisions": "#808080",
        "AI-Human Collisions": "#000000"     
    },
    post_process=customize_plot,
    backend="matplotlib"
)

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "height": 70,
    "width": 7,
}

epstein_model = HighwayV2VModel()

space_component = make_space_component(
    portrayal, post_process=post_process, draw_grid=True
)

page = SolaraViz(
    epstein_model,
    components=[space_component, collision_chart],
    model_params=model_params,
    name="Highway V2V Model",
)
page
