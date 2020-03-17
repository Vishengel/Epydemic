import argparse
from model import PyDemicModel

from server import init_server

def run_simulation(model_parameters):
    init_server(model_parameters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n_agents", metavar="N agents", type=int)
    args = parser.parse_args()

    print("Starting PyDemic simuation with %d agents" % args.n_agents)
    run_simulation(vars(args))