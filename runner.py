import random
from agent import Agent
from world import *
from decimal import Decimal, getcontext

    # World Setup
class SimParams():
    # instance used only to hold simulation level parameters
    def __init__(self, world_size, num_agents, resources, round_length):
        #world size is a square, rg 5*5
        self.world_size = world_size
        # num agents is count of agents
        self.num_agents = num_agents
        #resources are raw items that are refined to make artifcats
        self.resources = resources
        # round length is num turns in a single round
        self.round_length = round_length
    
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
    
def round_runner():
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
    
    sim_params = SimParams(world_size=5, num_agents=2, resources=resources,
            round_length=400)
    num_rounds_to_complete = "incomplete"

    # Build world, using world.py keep track of resource counts
    world = World(sim_params)
    
    #Display round starting state
    print("World Squares:")
    print(world.squares)
    print("Total num raw resources: ", world.raw_resource_count)
    print("Total num harvested resources: ", world.harvested_resource_count)
    
    # Setup Agents
    setup_agents_fn(sim_params, world)

    # End World Setup
    ################################################################################

    # Round Logic
    for round_num in range(sim_params.round_length):
        print("Starting round", round_num)
        print("====================")
        for agent in world.agent_list:
            agent.print_position()
            print(agent.id, " currently doing: ", agent.action)
            # grab agents' current square from world.squares
            # "next" grabs matching instance from iterator
            agent.position = next((square for square in world.squares if square.x == agent.x and
                square.y == agent.y), None)
    
            # main action: choose between moving, manipulating resources,
            # or something else (TBD); currently random, TODO: will change
            # sub action : choose a sub-action
            # e.g., move left, move up, harvest resource, trade resource, etc
            #this else needs to be refactored, redundant with lines below
            if agent.action == None:
                main_action = random.choice(agent.full_action_list)
    
            if main_action == agent.resource_actions:
                # i.e., if agent is choosing to do something with resources
                # then pass world.squares as an argument, round num for counter
                if agent.action == "harvesting":
                    if agent.position.square_resource:
                        print ("agent is harvesting!")
                        print ("harvesting started on round:", agent.action_start_time)
                        print ("harvesting will end on round:", agent.action_end_time)
                        if round_num > agent.action_end_time:
                            print("agent has finished harvesting",\
                                    agent.position.square_resource["name"])
                            agent.inventory.append(agent.position.square_resource)
                            agent.position.square_resource = None
                            world.harvested_resource_count += 1
                            world.raw_resource_count -= 1
                            if world.raw_resource_count == 0:
                                num_rounds_to_complete = round_num
                            agent.action = None
                        else:
                            print("agent is still harvesting", agent.position.square_resource)
                    else:
                        #if in harvesting but no resource
                        print("agent tried to harvest, but no resources found")
                        agent.action = None
    
                # if agent is doing a resource action besides harvesting (currently
                # aren't any such actions, pick randomly)
                else:
                    sub_action = random.choice(main_action)(agent, \
                            world.squares, round_num)
    
            elif main_action == agent.move_list:
                # i.e., if agent is moving, pass sim params to access world_size
                sub_action = random.choice(main_action)(agent, sim_params)
    
            agent.print_position()
            if agent.position.square_resource: \
                print("Square contains resource: ", \
                agent.position.square_resource["name"])
    
            print("^^^^^^^^^^")

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Simulation complete")
    print("Num raw resources initially: ", world.initial_raw_resource_count)
    print("Num raw resources remaining: ", world.raw_resource_count)
    print("Num harvested resources : ", world.harvested_resource_count)
    print("Turns taken to harvest all resos: ", num_rounds_to_complete)
    return [num_rounds_to_complete]
