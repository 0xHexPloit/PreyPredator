from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = dict()

    if type(agent) is Sheep:
        portrayal["Shape"] = "circle",
        portrayal["Color"] = "white",
        portrayal["Filled"] = True,
        portrayal["r"] = 1,
        portrayal["Layer"] = 1
        portrayal["text"] = agent.energy
        portrayal["text_color"] = "black"

    elif type(agent) is Wolf:
        portrayal["Shape"] = "circle",
        portrayal["Color"] = "#474747",
        portrayal["Filled"] = True,
        portrayal["r"] = 1,
        portrayal["Layer"] = 1
        portrayal["text"] = agent.energy
        portrayal["text_color"] = "white"

    elif type(agent) is GrassPatch:
        brown = r"#665937"
        light_green = r"#a6e0a7"
        green = r"#6ec270"
        dark_green = r"#369638"

        ratio = agent.steps_before_full_regrowth / agent.countdown

        if not agent.grown:
            color = brown
        elif agent.grown:
            color = dark_green
        elif ratio >= 0.5:
            color = light_green
        else:
            color = green

        portrayal["Shape"] = "rect",
        portrayal["Color"] = color,
        portrayal["Filled"] = False,
        portrayal["h"] = 1,
        portrayal["w"] = 1
        portrayal["Layer"] = 0

    return portrayal

model_params = dict(
    height=20,
    width=20,
    initial_sheep=UserSettableParameter("slider", "Initial sheep population", value=100, min_value=5, max_value=200),
    initial_wolves=UserSettableParameter("slider", "Initial wolves population", value=40, min_value=5, max_value=200),
    sheep_reproduce=UserSettableParameter("slider", "Sheep breeding probability", value=0.04, min_value=0.01, max_value=1.0, step=0.01),
    wolf_reproduce=UserSettableParameter("slider", "Wolf breeding probability", value=0.05, min_value=0.01, max_value=1.0, step=0.01),
    wolf_gain_from_food=UserSettableParameter("slider", "Energy gain from food (Wolf)", value=20, min_value=5, max_value=40),
    sheep_gain_from_food=UserSettableParameter("slider", "Energy gain from food (Sheep)",  value=4, min_value=2, max_value=10),
    grass_regrowth_time=UserSettableParameter("slider", "Grass regrowth time", value=30, min_value=5, max_value=50),
    initial_energy=UserSettableParameter("slider", "Initial energy", value=10, min_value=5, max_value=15),
    grass=UserSettableParameter("checkbox", "Grass Eatable", False),
    moore=UserSettableParameter("checkbox", "Moore displacement", value=True),
)

canvas_element = CanvasGrid(wolf_sheep_portrayal, model_params["height"], model_params["width"], 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)


server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
