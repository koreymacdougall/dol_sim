import random
import time
from agent import Agent
from decimal import Decimal, getcontext


# main world contructor fn
class World():
    def __init__(self, sim_params):
        # call square constructor with sim params
        self.squares = squares_builder_fn(sim_params.world_size, sim_params.resources)
        # set reso tallies to 0 at round start
        self.raw_resource_count = 0
        self.initial_raw_resource_count = 0
        self.harvested_resource_count = 0

        # tally resources at round start
        for s in self.squares:
            if s.square_resource:
                self.raw_resource_count += 1
                self.initial_raw_resource_count += 1

# setup all square obects, put them in array
class WorldSquare():
    def __init__(self, x, y, square_resource):
        self.x = x
        self.y = y
        self.square_resource = square_resource

    occupied = False
    occupant = None
    square_resource = None

# setup grid of squares
def squares_builder_fn(world_size, resources):
    squares = [ WorldSquare(x=x, y=y,
        square_resource=resource_selector_fn(resources)) for x in
            range(world_size) for y in range(world_size) ]
    return squares

# setup resource frequency distribution
def resource_freq_assign(resources, resources_list):
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

# determine which reso is on each square
def resource_selector_fn(resources):
    n = random.random()
    for resource in resources:
        if n > resource['lower'] and n <= resource['upper']:
            return resource
    return None

# setup agents
def setup_agents_fn(sim_params, world):
    # TODO - stop agents from being on same square!
    # TODO - if two spawn on same square, can cause "over harvesting"
    world.agent_list=[]
    for i in range(sim_params.num_agents):
        unplaced = True
        # randomly choose squares (coords) until an empty one picked
        while unplaced:
            x_pos = random.choice(range(sim_params.world_size))
            y_pos = random.choice(range(sim_params.world_size))
            target = next((square for square in world.squares \
                if square.x == x_pos and square.y == y_pos), None)
            if not target.occupied:
                target.occupied = True
                unplaced = False

        world.agent_list.append(Agent(
            x=x_pos,
            y=y_pos,
            id=i,
            # TODO - implement action durations
            harvest_duration = 2,
            refine_duration = 5,
            learning_rate = 1,
            world = world
            ))
        target.occupant = world.agent_list[-1]

def draw_world(sim_params, world, round_num):
    print("starting round ", round_num)
    map_string = ""
    # horizontal divider added between every row
    map_string_horizontal_divider = "\t" + sim_params.world_size * (5 * "-" + " ")
    map_string += map_string_horizontal_divider
    map_string += "\n"
    for y in reversed(range(sim_params.world_size)):
        row = [square for square in world.squares if square.y == y]
        map_string += "y:" + str(y)+ "\t" 
        for sq in row:
            if sq.occupied:
                occupant = sq.occupant.id
            else:
                occupant = " "
            if sq.square_resource:
                reso = sq.square_resource["name"][-1]
            else:
                reso = " "
            map_string += "|{}|{}| ".format(occupant, reso)

        map_string += "\n" + map_string_horizontal_divider + "\n"
        # map_string += 
        # map_string += "\n"
        # print(sq.x, sq.y)
        # if sq.occupied:
        #     print("#####\n#{}|{}#\n#####".format(sq.occupant.id, "="))
        # else:
        #     print("#####\n#{}|{}#\n#####".format("-", "="))
    
    # map_string += "\t x:r   x:2   x:3   x:4"
    bottom_string = "\t "
    for col in range(sim_params.world_size):
        piece = "x:" + str(col) + "   "
        bottom_string += piece
    map_string += bottom_string

    print(map_string)
    time.sleep(2)

