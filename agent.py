class Agent():
    """ Macro-Cognitive Agent definition
        Several paramters affecting performance:
        Memory decay rate (from lit)
        Learning / skill mastery rate(from lit)
        Knowledge interference levels?
    """

    def __init__(self, x, y, id, harvest_duration,
            refine_duration, learning_rate, world):
        self.x = x
        self.y = y
        # next method, iterator fn, seems like ruby's first fn
        self.position = next((square for square in world.squares if square.x ==\
            self.x and square.y == self.y), None)
        print (self.x, self.y, self.position.x, self.position.y)
        self.id = id
        self.inventory = []
        # harvest duration may be a sim param, may be a skill param, that can
        # vary per agent
        self.harvest_duration = harvest_duration
        self.refine_duration = refine_duration
        self.action = ""
        # learning rate will determine how quickly skills improve
        # higher rate, sooner to reach the next level of master
        # Note - this will be a step-wise learning model, with discrete jumps
        self.learning_rate = learning_rate

        #memory to be built
        memory = {}
        
        # TODO: parameterized skills to be built

    # agent movement definitions ##############################################
    # note that world wraps around on both axes

    def move_left(self, sim_params):
        print("Moving agent", self.id, "left")
        if self.x - 1 >= 0:
            self.x -= 1
        else:
            self.x = sim_params.world_size - 1

    def move_right(self, sim_params):
        print("Moving agent", self.id, "right")
        if self.x + 1 <= sim_params.world_size - 1:
            self.x += 1
        else:
            self.x = 0

    def move_down(self, sim_params):
        print("Moving agent", self.id, "down")
        if self.y - 1 >= 0:
            self.y -= 1
        else:
            self.y = sim_params.world_size - 1

    def move_up(self, sim_params):
        print("Moving agent", self.id, "up")
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

    # resource_actions defines what agents can do with resources
    # for now, resource action list is only harvest
    resource_actions = [harvest]
    #resource_actions = [harvest, trade, refine]

    # skill_list
    # skill_list = []
    # This might involve interaction with memory...

    # full action list is a combination of all the possible actions:
    # move & resource action for now
    full_action_list = [move_list, resource_actions]

    # print agent position to screen
    def print_position(self):
      print("Agent ", self.id, " position x,y:", self.x, self.y)       
