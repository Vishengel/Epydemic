import config

from mesa.visualization.ModularVisualization import ModularServer

from model import PyDemicModel
from SimpleContinuousModule import SimpleCanvas


def agent_draw(agent):
    portrayal = {"Shape": "circle", "r": config.agent_radius, "Filled": "true", "Color": "Red"}

    if agent.infected:
        portrayal["Color"] = "Green"

    if agent.cured:
        portrayal["Color"] = "Blue"

    return portrayal

def init_server(model_parameters):
    pydemic_canvas = SimpleCanvas(agent_draw, 500, 500)
    server = ModularServer(PyDemicModel, [pydemic_canvas], name="PyDemic", model_params=model_parameters)
    server.launch()