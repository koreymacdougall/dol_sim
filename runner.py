import random
from agent import Agent
from world import WorldSquare, world_builder_fn#, resource_distributor

################################################################################
# World Setup
class SimParams():
    # used only to hold simulation level parameters
    def __init__(self, world_size, num_agents, resources):
        self.world_size = world_size
        self.num_agents = num_agents
        self.resources = resources

# create sim_param instance to hold class variables
# this is main line(s) to set up sim-wide params

#TODO - move resource allocation into world.py ?
resources_list = [        
        ['resource a', 0.1],
        ['resource b', 0.1],
        ['resource c', 0.1],
        ['resource d', 0.2],
        ['resource e', 0.4]
        ]

resources = [ {'name': r[0],  'freq': r[1], 'lower': None, 'upper':
    None } for r in resources_list ]

for reso in resources_list:
    lower = 0
    index = resources_list.index(reso)
    if index == 0:
        for r in resources:
            if r['name'] == reso[0]:
                r['lower'] = 0
                r['upper'] = reso[1]
    else:
        for sub_reso in resources_list[0:index]:
            lower += sub_reso[1]
        for r in resources:
            if r['name'] == reso[0]:
                r['lower'] = lower
                r['upper'] = lower + r['freq']


sim_params = SimParams(world_size=5, num_agents=2, resources=resources)

# Build world
world_squares = world_builder_fn(sim_params.world_size, sim_params.resources)
print(world_squares)
for s in world_squares:
    print(s.square_resource, s.x, s.y)
quit()

# Setup Agents
agent_list=[]
for i in range(sim_params.num_agents):
    agent_list.append(Agent(
        x=random.choice(range(sim_params.world_size)),
        y=random.choice(range(sim_params.world_size)),
        agent_id=i,
        ws=sim_params.world_size)) 


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
        random.choice(agent.move_list)(agent)
        # grab square from world_squares
        # NOTE: feels hackish after using ruby/where
        # acs = agents_current_square
        # next grabs matching instance from iterator
        acs = next((square for square in world_squares if square.x == agent.x and
            square.y == agent.y), None)
        agent.print_position()
        if acs.square_resource:
            print("Square contains resource: ", acs.square_resource)

        print("^^^^^^^^^^")
