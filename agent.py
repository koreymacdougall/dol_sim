class Agent():
    """ Macro Cognitive Agent definition
        several paramters affecting performance:
        memory decay rate (from lit)
        learning / skill mastery rate(from lit)
        knowledge interference levels?
    """
    def __init__(self, x, y, agent_id, ws):
        self.x = x
        self.y = y
        self.agent_id = agent_id
        # world_size only really needs to be defined for a single agent
        # but having it as a class param is/seems useful for movement
        global world_size
        world_size = ws
        inventory = {}

    #memory to be built
    memory = {}

    #agent movements
    #note that world wraps around on both axes

    def move_left(self):
        print("Moving agent", self.agent_id, "left")
        if self.x - 1 >= 0:
            self.x -= 1
        else:
            self.x = world_size - 1

    def move_right(self):
        print("Moving agent", self.agent_id, "right")
        if self.x + 1 <= world_size - 1:
            self.x += 1
        else:
            self.x = 0

    def move_down(self):
        print("Moving agent", self.agent_id, "down")
        if self.y - 1 >= 0:
            self.y -= 1
        else:
            self.y = world_size - 1

    def move_up(self):
        print("Moving agent", self.agent_id, "up")
        if self.y + 1 <= world_size - 1:
            self.y += 1
        else:
            self.y = 0

    # move_list defines how agents can move around the map
    move_list = [move_left, move_right, move_down, move_up]

    # action_list defines what agents can do with resources
    #action_list = [harvest, trade, refine]

    # skill_list
    # TBD
    # This might involve interaction with memory...

    # print agent position to screen
    def print_position(self):
      print("Agent ", self.agent_id, " position x,y:", self.x, self.y)       
