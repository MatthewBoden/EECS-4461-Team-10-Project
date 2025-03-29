from agent import (
    AIVehicle,
    HumanVehicle,
)
from model import HighwayV2VModel
from mesa.visualization.utils import update_counter
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
import solara

def portrayal(agent):
    if agent is None:
        return

    model = agent.model
    coordinate = agent.cell.coordinate

    portrayal = { 
        "size": 75, 
        "marker": "^"
    }

    if isinstance(agent, AIVehicle):
        portrayal["color"] = "#AA4A44"
    elif isinstance(agent, HumanVehicle):
        portrayal["color"] = "#808080"

    
    if coordinate in model.collided_cells:
        cell = agent.cell
        agents_in_cell = cell.agents
        
        has_ai = any(isinstance(a, AIVehicle) for a in agents_in_cell)
        has_human = any(isinstance(a, HumanVehicle) for a in agents_in_cell)
        
        if has_ai and has_human:
            # AI-Human collision
            portrayal["marker"] = "*" # star shape
            portrayal["color"] = "#FF0000" # red
            portrayal["size"] = 85
        elif has_ai and not has_human:
            # AI-AI collision
            portrayal["marker"] = "*" 
            portrayal["color"] = "#AA00AA" # purple
            portrayal["size"] = 85
        elif has_human and not has_ai:
            # Human-Human collision
            portrayal["marker"] = "*" 
            portrayal["color"] = "#FF9900" # yellow
            portrayal["size"] = 85
            

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


def customize_plot_4(ax):
    ax.set_title("Lane Change Success Rate Over Time")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Number of Lane Changes")
    ax.legend(loc="upper left")
    ax.get_figure().set_size_inches(8, 4)    


def space_filler_plot(ax):
    ax.get_figure().set_visible(False)

collision_chart = make_plot_component(
    {
        "AI-AI Collisions": "#AA00AA",
        "Human-Human Collisions": "#FF9900",
        "AI-Human Collisions": "#FF0000"     
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

success_lane_chart = make_plot_component(
    {
        "Potential Collisions Avoided": "#5B9BD5",
        "Successful Lane Changes": "#27AE60",
        "Failed Lane Changes": "#E74C3C",
    },
    post_process=customize_plot_4,
    backend="matplotlib"
)

@solara.component
def agent_counter(model):
    update_counter.get()
    
    with solara.Div(style={"margin-top": "50px", "margin-left": "-100px"}): 
        with solara.Row(justify="center", style={"margin-bottom": "20px"}):
            solara.Text("AGENT COUNTS", style={
                "font-size": "36px",
                "font-weight": "bold",
                "color": "#2C3E50",
                "text-align": "center",
                "letter-spacing": "2px"
            })
            
        with solara.Row(
            justify="center",
            gap="20px",
            style={"padding": "20px"} 
        ):
            with solara.Card("AI Agents", style={
                "background": "#AA4A44", 
                "color": "white", 
                "min-width": "150px",
                "padding": "15px",
                "text-align": "center"
            }):
                solara.Text(str(model.ai_count), style={
                    "font-size": "32px", 
                    "text-align": "center",
                    "font-weight": "bold"
                })
            
            with solara.Card("Human Agents", style={
                "background": "#808080", 
                "color": "white", 
                "min-width": "150px",
                "padding": "15px",
                "text-align": "center"
            }):
                solara.Text(str(model.human_count), style={
                    "font-size": "32px", 
                    "text-align": "center",
                    "font-weight": "bold"
                })
            
            with solara.Card("Total Agents", style={
                "background": "#5B9BD5",
                "color": "white", 
                "min-width": "150px",
                "padding": "15px",
                "text-align": "center",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
            }):
                solara.Text(str(model.human_count + model.ai_count), style={
                    "font-size": "32px", 
                    "text-align": "center",
                    "font-weight": "bold"
                })
            
            # with solara.Card("Potential Avoided/Detected Collisions", style={"background": "#5B9BD5", "color": "white", "min-width": "150px", "padding": "15px", "text-align": "center"}):
            #     solara.Text(str(model.potential_collisions_avoided), style={"font-size": "32px", "text-align": "center", "font-weight": "bold"})
            
            # with solara.Card("Successful Lane Changes", style={"background": "#E74C3C", "color": "white", "min-width": "150px", "padding": "15px", "text-align": "center"}):
            #     solara.Text(str(model.successful_lane_changes), style={"font-size": "32px", "text-align": "center", "font-weight": "bold"})

            # with solara.Card("Failed Lane Changes", style={"background": "#E74C3C", "color": "white", "min-width": "150px", "padding": "15px", "text-align": "center"}):
            #     solara.Text(str(model.failed_lane_changes), style={"font-size": "32px", "text-align": "center", "font-weight": "bold"})

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
    "ai_malfunction_rate": Slider("AI Malfunction Rate", 0, 0.0, 100, 1),
    "left_sway_coefficient": Slider("V2V Left Sway Coefficient", 0.5, 0.0, 1, 0.01),
    "right_sway_coefficient": Slider("V2V Right Sway Coefficient", 0.5, 0.0, 1, 0.01),
}

epstein_model = HighwayV2VModel()

space_component = make_space_component(
    portrayal, post_process=post_process, draw_grid=True
)

page = SolaraViz(
    epstein_model,
    components=[
        space_component,
        agent_counter,
        space_fill,
        polar_lane_average,
        space_fill,
        collision_chart,
        space_fill,
        success_lane_chart
    ],
    model_params=model_params,
    name="Highway V2V Model",
)
page
