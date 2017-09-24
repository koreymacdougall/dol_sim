class Agent():
    """ Macro-Cognitive Agent definition
        Several paramters affecting performance:
        Memory decay rate (from lit)
        Learning / skill mastery rate(from lit)
        Knowledge interference levels?
    """


#global world_size

    def __init__(self, x, y, agent_id, world_squares, harvest_duration):
        world_squares = world_squares
        self.x = x
        self.y = y
        # use next method, iterator fn, seems like ruby's first fn
        self.position = next((square for square in world_squares if square.x ==
            self.x and square.y == self.y), None)
        print (self.x, self.y, self.position.x, self.position.y)
        self.agent_id = agent_id
        self.inventory = {}
        self.harvest_duration = harvest_duration
        self.action = ""

        #memory to be built
        memory = {}
        
        # TODO: parameterized skills to be built

    # agent movement definitions ##############################################
    # note that world wraps around on both axes

    def move_left(self, sim_params):
        print("Moving agent", self.agent_id, "left")
        if self.x - 1 >= 0:
            self.x -= 1
        else:
            self.x = sim_params.world_size - 1

    def move_right(self, sim_params):
        print("Moving agent", self.agent_id, "right")
        if self.x + 1 <= sim_params.world_size - 1:
            self.x += 1
        else:
            self.x = 0

    def move_down(self, sim_params):
        print("Moving agent", self.agent_id, "down")
        if self.y - 1 >= 0:
            self.y -= 1
        else:
            self.y = sim_params.world_size - 1

    def move_up(self, sim_params):
        print("Moving agent", self.agent_id, "up")
        if self.y + 1 <= sim_params.world_size - 1:
            self.y += 1
        else:
            self.y = 0

    # agent resource action definitions #######################################

    def harvest(self, world_squares, round):
        if self.position.square_resource:
            print("harvesting resource: ", self.position.square_resource)
            print("initilizing the harvest!!")
            self.action = "harvesting"
            self.action_start_time = round
            self.action_end_time = round + self.harvest_duration

    def trade(self, world_squares):
        pass

# resources is a list of dicts that store inp
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
