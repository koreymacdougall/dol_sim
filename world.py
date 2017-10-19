import random
import time

class WorldSquare():
    def __init__(self, x, y, square_resource):
        self.x = x
        self.y = y
        self.square_resource = square_resource

    occupied = False
    occupant = None
    square_resource = None

class World():
    def __init__(self, sim_params):
        self.squares = squares_builder_fn(sim_params.world_size, sim_params.resources)
        self.raw_resource_count = 0
        self.initial_raw_resource_count = 0
        self.harvested_resource_count = 0

        #tally resources at round start
        for s in self.squares:
            if s.square_resource:
                self.raw_resource_count += 1
                self.initial_raw_resource_count += 1

# setup grid of squares

def squares_builder_fn(world_size, resources):
    squares = [ WorldSquare(x=x, y=y,
        square_resource=resource_selector_fn(resources)) for x in
            range(world_size) for y in range(world_size) ]

    return squares

# determine which reso is on each square
def resource_selector_fn(resources):
    n = random.random()
    for resource in resources:
        if n > resource['lower'] and n <= resource['upper']:
            print(n, " is between ", resource['lower'], " and ", resource['upper'])
            return resource
    return None



