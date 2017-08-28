import random
from agent import Agent
from world import WorldSquare, world_builder_fn

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

resources_list = [        
        ['resource a', 0.1],
        ['resource b', 0.1],
        ['resource c', 0.1]
        ]
resources = [ {'name': r[0],  'freq': r[1], 'lower': None, 'upper':
    None } for r in resources_list ]

print(resources)
#resource_disribution = {}
#dist_total = 0
#for r in resources:
    #resource_disribution.append(r: range(dist_total, dist_total + r))
    #print (resources[r])
    #print (resource_disribution)
quit()

sim_params = SimParams(world_size=5, num_agents=2, resources=resources)

# Build world
world_squares = world_builder_fn(sim_params.world_size, sim_params.resources)
print(world_squares)

# Setup Agents
agent_list = [Agent 
    (x=random.choice(range(sim_params.world_size)),
    y=random.choice(range(sim_params.world_size)), 
    agent_id=i,
    ws=sim_params.world_size) 
    for i in range(5)]

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
