import random
from agent import Agent
from world import WorldSquare

################################################################################
# World Setup
class SimParams():
    # used only to hold simulation level parameters
    def __init__(self, world_size, num_agents):
        self.world_size = world_size
        self.num_agents = num_agents
# create instance to hold class variables
# this is main line to set up sim-wide params
sim_params = SimParams(world_size=5, num_agents=2)

# setup grid of squares
world_squares = [WorldSquare(x=x, y=y) for x in range(sim_params.world_size) for y in
        range(sim_params.world_size)]

# Setup Agents
agent_list = [Agent(x=0, y=0, agent_id=i, ws=sim_params.world_size) for i in range(sim_params.num_agents)]              

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
        agent.print_position()
        print("^^^^^^^^^^")
                                                                                                                        
                               
