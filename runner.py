import random
import time
from agent import Agent
from world import *
from decimal import Decimal, getcontext

    # World Setup
class SimParams():
    # instance used only to hold simulation level parameters
    def __init__(self, world_size, num_agents, resources, rounds_per_run,
            num_rounds_to_completion):
        #world size is a square, rg 5*5
        self.world_size = world_size
        # num agents is count of agents
        self.num_agents = num_agents
        #resources are raw items that are refined to make artifcats
        self.resources = resources
        # round length is num turns in a single round
        self.rounds_per_run = rounds_per_run
        self.num_rounds_to_completion = num_rounds_to_completion
    
    #Resources w/ Frequencies distributions 

    # temp notes:
    # this list to be set up by experimenter; 
    # resources, below, are what's used in sim
    # resource frequencies will be variableized
    # resource density will be determined by:
    # set total avail, then randomly assign subsets of the resource
    # eg total = 0.4, a = rand(0, 0.4), total_rem = total - 0 - a.freg
    # repeat for all reso's, could say that if early ones take up entire range, 
    # other ones get some super small value (0.01 or s/t)
    
def single_run_runner(num_agents):
    # r[0[ = name, r[1] = chance of occurrence, rounded to 2 sig digits]
    resources_list = [
            ['resource a', round(Decimal(0.1), 2)],
            ['resource b', round(Decimal(0.1), 2)],
            ['resource c', round(Decimal(0.2), 2)]
            ]

    # Stick all resources into an array of dicts
    # store name, freq, and upper & lower bounds, initially empty
    # TODO- make this a fn, and move it into world.py
    resources = [ {'name': r[0],  'freq': r[1], 'lower': None, 'upper':
        None } for r in resources_list ]

    # set up the resources w/ probability distribtions, based on frequencies
    # these are non-overlapping windows, used to determine, w/ a random
    # number, which reso is on which square
    resource_freq_assign(resources, resources_list)

    # Main line(s) to set up sim-wide params
    # TODO - move num_rounds_to_completion to somwhere else...
    sim_params = SimParams(\
            world_size=5,\
            num_agents=num_agents,\
            resources=resources,\
            rounds_per_run=800,\
            num_rounds_to_completion="inc")
    

    # Build world, using world.py keep track of resource counts
    world = World(sim_params)
    
    # Setup Agents
    setup_agents_fn(sim_params, world)

    # End World Setup
    ################################################################################

    # Round Logic
    for round_num in range(sim_params.rounds_per_run):
        if sim_params.num_rounds_to_completion == "inc":
            for agent in world.agent_list:
                agent.act(world, round_num, sim_params)
                ("^^^^^^^^^^")
            draw_world(sim_params, world, round_num)
        else:
            pass

    return sim_params.num_rounds_to_completion,\
            world.initial_raw_resource_count,\
            world.harvested_resource_count
