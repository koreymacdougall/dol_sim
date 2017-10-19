import random
from decimal import Decimal, getcontext
from agent import Agent
from world import World, WorldSquare, squares_builder_fn

################################################################################
# World Setup

class SimParams():
    # instance used only to hold simulation level parameters
    def __init__(self, world_size, num_agents, resources, round_length):
        #world size is a square, rg 5*5
        self.world_size = world_size
        # num agents is count of agents
        self.num_agents = num_agents
        #resources are raw items that are modified to make artifcats
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

# r[0[ = name, r[1] = chance of occurrence, rounded to 2 sig digits]
resources_list = [
        ['resource a', round(Decimal(0.1), 2)],
        ['resource b', round(Decimal(0.1), 2)],
        ['resource c', round(Decimal(0.2), 2)]
        ]

# Stick all resources into an array of dicts
# store name, freq, and upper & lower bounds, initially empty
resources = [ {'name': r[0],  'freq': r[1], 'lower': None, 'upper':
    None } for r in resources_list ]

# set up the resources probability distribtions, based on frequencies
# these are non-overlapping windows, used to determine, w/ a random
# number, which reso is on which square

for reso in resources_list:
    lower = 0
    index = resources_list.index(reso)
    if index == 0:
        for r in resources:
            if r['name'] == reso[0]:
                r['lower'] = round(Decimal(0), 2)
                r['upper'] = reso[1]
    else:
        for sub_reso in resources_list[0:index]:
            lower += sub_reso[1]
        for r in resources:
            if r['name'] == reso[0]:
                r['lower'] = lower
                r['upper'] = lower + r['freq']

# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# world_sizes = []
# num_agents = []
# round_lengths =[]

# Main line(s) to set up sim-wide params

sim_params = SimParams(world_size=5, num_agents=2, resources=resources,
        round_length=100)

# Build world, using world.py keep track of resource counts
world = World(sim_params)

#Display round starting state
print("World Squares:")
print(world.squares)

print("Total num raw resources: ", world.raw_resource_count)
print("Total num harvested resources: ", world.harvested_resource_count)


# Setup Agents
agent_list=[]
for i in range(sim_params.num_agents):
    agent_list.append(Agent(
        x=random.choice(range(sim_params.world_size)),
        y=random.choice(range(sim_params.world_size)),
        id=i,
        harvest_duration = 2,
        refine_duration = 5,
        learning_rate = 1,
        world = world
        ))



# End World Setup
################################################################################

# Round Logic
for round in range(sim_params.round_length):
    print("Starting round", round)
    print("====================")
    for agent in agent_list:
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
        if agent.action == "":
            main_action = random.choice(agent.full_action_list)

        if main_action == agent.resource_actions:
            # i.e., if agent is choosing to do something with resources
            # then pass world.squares as an argument, round num for counter
            if agent.action == "harvesting":
                if agent.position.square_resource:
                    print ("agent is harvesting!")
                    print ("harvesting started on round:", agent.action_start_time)
                    print ("harvesting will end on round:", agent.action_end_time)
                    if round > agent.action_end_time:
                        print("agent has finished harvesting",\
                                agent.position.square_resource["name"])
                        agent.inventory.append(agent.position.square_resource)
                        agent.position.square_resource = None
                        world.harvested_resource_count += 1
                        world.raw_resource_count -= 1
                        agent.action = ""
                    else:
                        print("agent is still harvesting", agent.position.square_resource)
                else:
                    #if in harvesting but no resource
                    print("agent tried to harvest, but no resources here")

            # if agent is doing a resource action besides harvesting (currently
            # aren't any such actions, pick randomly)
            else:
                sub_action = random.choice(main_action)(agent, world.squares, round)

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
