from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization import Slider
from traffic_simulator import TrafficModel, Car, Semaphore

def traffic_draw(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "Layer": 0,
        "w": 1,
        "h": 1,
        "Color": "red"
    }

    if isinstance(agent, Car):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
        portrayal["Color"] = "BLACK"
    elif isinstance(agent, Semaphore):
        if agent.state == 0:
            portrayal["Color"] = "red"
        elif agent.state == 1:
            portrayal["Color"] = "yellow"
        elif agent.state == 2:
            portrayal["Color"] = "green"

    return portrayal


"""
green_duration = 10  # Valor inicial para la duración del semáforo en estado verde
red_duration = 10  # Valor inicial para la duración del semáforo en estado rojo
num_agents = 5  # Valor inicial para el número de carros
"""
model_params = {
    "width": 20,
    "height": 10,
    "N": Slider("Number of cars", 2, 1, 10),
    "green_duration": Slider("Green Duration", 10, 1, 20),
    "red_duration": Slider("Red Duration", 10, 1, 20)
}
grid = CanvasGrid(traffic_draw, 20, 10, 400, 400)

chart = ChartModule( [{"Label": "green_duration", "Color": "red",}], data_collector_name='datacollector')

"""
server = ModularServer(
    TrafficModel,
    [grid, chart],
    "Traffic Model",
    {
        "width": 20,
        "height": 10,
        "N": num_agents,
        "green_duration": green_duration,
        "red_duration": red_duration
    }
)
"""
server = ModularServer(
    TrafficModel,
    [grid, chart],
    "Traffic Model",
    model_params
)


server.port = 8521
server.launch()

# Run the server with the following command:
# python server.py