class Agent():
    """ Macro Cognitive Agent definition
        Several paramters affecting performance:
        Memory decay rate (from lit)
        Learning / skill mastery rate(from lit)
        Knowledge interference levels?
    """

    def __init__(self, x, y, agent_id, ws):
        self.x = x
        self.y = y
        self.current_square = None
        self.agent_id = agent_id
        self.inventory = {}
        # world_size only really needs to be defined for a single agent
        # but having it as a class param is/seems useful for movement
        global world_size
        world_size = ws

        #memory to be built
        memory = {}

    # agent movement definitions ##############################################
    # note that world wraps around on both axes

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

    # agent resource action definitions #######################################

    def harvest(self, world_squares):
        if self.current_square.square_resource:
            print("made it into harvest fn")
            quit()
        print("harvesting resource: ")

    def trade(self, world_squares):
        pass

    def refine(self, world_squares):
        pass

    # move_list defines how agents can move around the map
    move_list = [move_left, move_right, move_down, move_up]

    # resource_action_list defines what agents can do with resources
    # for now, resource action list is only harvest
    resource_action_list = [harvest]
    #resource_action_list = [harvest, trade, refine]

    # skill_list
    # skill_list = []
    # This might involve interaction with memory...

    # full action list is a combination of all the possible actions:
    # move & resource action for now
    full_action_list = [move_list, resource_action_list]

    # print agent position to screen
    def print_position(self):
      print("Agent ", self.agent_id, " position x,y:", self.x, self.y)       
