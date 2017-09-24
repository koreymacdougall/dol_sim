import random
from decimal import Decimal, getcontext
from agent import Agent
from world import WorldSquare, world_builder_fn

################################################################################
# World Setup

class SimParams():
    # instance used only to hold simulation level parameters
    def __init__(self, world_size, num_agents, resources):
        self.world_size = world_size
        self.num_agents = num_agents
        self.resources = resources

# create sim_param instance to hold class variables
# this is main line(s) to set up sim-wide params

# this is to be set by experimenter; resources, below, are what's used in sim
resources_list = [
        ['resource a', round(Decimal(0.1), 2)],
        ['resource b', round(Decimal(0.1), 2)],
        ['resource c', round(Decimal(0.2), 2)]
        ]

resources = [ {'name': r[0],  'freq': r[1], 'lower': None, 'upper':
    None } for r in resources_list ]

# set up the resources probability distribtions, based on frequencies
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

# instantiate an instance to store global simulation parameters
sim_params = SimParams(world_size=5, num_agents=2, resources=resources)

# Build world
world_squares = world_builder_fn(sim_params.world_size, sim_params.resources)
resource_counter = 0
print("World Squares:")
print(world_squares)
for s in world_squares:
    print(s.square_resource, s.x, s.y)
    if s.square_resource:
        resource_counter += 1

print("Total num resources: ", resource_counter)

# Setup Agents
agent_list=[]
for i in range(sim_params.num_agents):
    agent_list.append(Agent(
        x=random.choice(range(sim_params.world_size)),
        y=random.choice(range(sim_params.world_size)),
        agent_id=i,
        world_squares = world_squares,
        harvest_duration = 2,
        ))


# number of turns for a single run
sim_params.round_length = 5

# End World Setup
################################################################################

# Round Logic
for round in range(sim_params.round_length):
    print("Starting round", round)
    print("====================")
    for agent in agent_list:
        agent.print_position()
        print(agent.action)
        # grab agents' current square from world_squares
        # "next" grabs matching instance from iterator
        agent.position = next((square for square in world_squares if square.x == agent.x and
            square.y == agent.y), None)
        # main action: choose between moving, manipulating resources,
        # or something else (TBD); currently random, TODO: will change
        # sub action : choose a sub-action
        # e.g., move left, move up, harvest resource, trade resource, etc

        if agent.action == "":
            main_action = random.choice(agent.full_action_list)
        else:
            main_action = agent.resource_action_list

        if main_action == agent.resource_action_list:
            # i.e., if agent is choosing to do something with resources
            # then pass world_squares as an argument, round num for counter
            if agent.action == "harvesting":
                print ("agent is harvesting!")
                print ("harvesting started on round:", agent.action_start_time)
                print ("harvesting will end on round:", agent.action_end_time)
                if round >= agent.action_end_time:
                    print("agent has finished harvesting", agent.position.square_resource)
                    quit()
                else:
                    print("agent is still harvesting", agent.position.square_resource)

            else:
                sub_action = random.choice(main_action)(agent, world_squares, round)
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
