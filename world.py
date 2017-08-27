import random
class WorldSquare():
    def __init__(self, x, y, square_resource):
        self.x = x
        self.y = y
        self.square_resource = square_resource

    occupied = False
    occupant = None

# setup grid of squares
def world_builder_fn(world_size, resources):
    world = [ WorldSquare(x=x, y=y, square_resource=random.choice(resources)) for x in
            range(world_size) for y in range(world_size) ]
    return world
