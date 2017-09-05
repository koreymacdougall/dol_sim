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

# setup grid of squares
def world_builder_fn(world_size, resources):
    world = [ WorldSquare(x=x, y=y,
        square_resource=resource_selector_fn(resources)) for x in
            range(world_size) for y in range(world_size) ]
    return world

def resource_selector_fn(resources):
    n = random.random()
    for resource in resources:
        if n > resource['lower'] and n <= resource['upper']:
            print(n, " is between ", resource['lower'], " and ", resource['upper'])
            return resource
    return None



