import random
import time

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
        #print(self.x, self.y, self.position.x, self.position.y)
        self.id = id
        self.inventory = []
        # harvest duration may be a sim param, may be a skill param, that can
        # vary per agent
        self.harvest_duration = harvest_duration
        self.refine_duration = refine_duration
        self.action_type = None
        self.sub_action = None
        self.action_start_time = None
        self.action_end_time = None
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
        #print("Moving agent", self.id, "left")
        if self.x - 1 >= 0:
            self.x -= 1
        else:
            self.x = sim_params.world_size - 1

    def move_right(self, sim_params):
        #print("Moving agent", self.id, "right")
        if self.x + 1 <= sim_params.world_size - 1:
            self.x += 1
        else:
            self.x = 0

    def move_down(self, sim_params):
        #print("Moving agent", self.id, "down")
        if self.y - 1 >= 0:
            self.y -= 1
        else:
            self.y = sim_params.world_size - 1

    def move_up(self, sim_params):
        #print("Moving agent", self.id, "up")
        if self.y + 1 <= sim_params.world_size - 1:
            self.y += 1
        else:
            self.y = 0

    def filter_moves(self, world, sim_params):
        # check which moves are allowable before choosing one
        # note: could do this by finding the neighbour squares instead
        current_loc = self.position
        # print("testing")
        # print("self position is...")
        # print(current_loc.x, current_loc.y)
        # time.sleep(1)

        # check up movement
        if self.y == sim_params.world_size-1:
            up_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == 0), None)
            # print("worked up wrap")
            # print(up_target)
        else:
            up_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == self.y + 1), None)
            # print("worked up")
            # print(up_target)

        # check down movement
        if self.y == 0:
            down_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == sim_params.world_size-1), None)
            # print("worked down wrap")
            # print(down_target)
        else:
            down_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == self.y - 1), None)
            # print("worked down")
            # print(down_target)

        # check right movement
        if self.x == sim_params.world_size-1:
            right_target = next((square for square in world.squares if\
            square.x == 0 and square.y == self.y), None)
            # print("worked right wrap")
            # print(right_target)
        else:
            right_target = next((square for square in world.squares if square.x ==\
            self.x + 1 and square.y == self.y), None)
            # print("worked right")
            # print(right_target)

        # check left movement
        if self.x == 0:
            left_target = next((square for square in world.squares if square.x ==\
            sim_params.world_size-1 and square.y == self.y), None)
            # print("worked left wrap")
            # print(left_target)
        else:
            left_target = next((square for square in world.squares if square.x ==\
            self.x - 1  and square.y == self.y), None)
            # print("worked left")
            # print(left_target)

        # print("did the filtering")
        # print("up, down, right, left")
        # print(up_target.x, up_target.y, down_target.x, down_target.y)
        # print(left_target.x, left_target.y, right_target.x, right_target.y)
        # time.sleep(2)

        # targets = [up_target, down_target, right_target, left_target]

        if not up_target.occupied:
            self.filtered_move_list.append(self.move_up)
        if not down_target.occupied:
            self.filtered_move_list.append(self.move_down)
        if not right_target.occupied:
            self.filtered_move_list.append(self.move_right)
        if not left_target.occupied:
            self.filtered_move_list.append(self.move_left)







    # agent resource action definitions #######################################
    def harvest(self, round_num, world, sim_params):
        # if agent has already started a harvest
        if self.action_end_time != None:
            # check if harvest is finished
            if round_num > self.action_end_time:
                #print("agent has finished harvesting", self.position.square_resource["name"])
                # add harvested resource to inentory
                self.inventory.append(self.position.square_resource)
                # remove resource from world square
                self.position.square_resource = None
                # add 1 to count of harvested resources
                world.harvested_resource_count += 1
                # subtract 1 from count of raw / unharvested resources
                world.raw_resource_count -= 1

                # if all resources have now been harvested, 
                # return current round number as num_rounds_to_completion
                if world.raw_resource_count == 0:
                    sim_params.num_rounds_to_completion = round_num

                # reset self.action to none
                self.action_type = None
                self.sub_action = None
                self.action_end_time = None
                self.action_start_time = None
                self.filtered_move_list = []
        
            # if agent hasn't finished req'd num of harvest rounds ...
            # don't change action yet
            else:
                #print("self is still harvesting", self.position.square_resource)
                pass

        #if agent hasn't started harvest, check if resource present
        else:
            if self.position.square_resource:
                self.action_start_time = round_num
                self.action_end_time = round_num + self.harvest_duration

            # if agent attempts to harvest, but no reso present ...
            # turn is basically wasted
            else:
                #print("self tried to harvest, but no resources found")
                self.action_type = None

    def trade(self, world_squares):
        pass

    def refine(self, world_squares):
        pass

    # move_list defines how agents can move around the map
    move_list = [move_left, move_right, move_down, move_up]
    # multiple agents cannot occupy the same square

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
      #print("Agent ", self.id, " position x,y:", self.x, self.y)       
      pass

    def act(self, world, round_num, sim_params):
        self.filtered_move_list = []
        self.print_position()
        #print(self.id, " currently doing: ", self.action_type, self.sub_action)
        if self.position.square_resource:
            #print("Square contains resource: ", self.position.square_resource["name"])
            pass

        # grab agent's current square from world.squares
        # "next" grabs matching instance from iterator
        self.position = next((square for square in world.squares \
            if square.x == self.x and square.y == self.y), None)

        # self.action_type: choose between moving, manipulating resources,
        # or something else (TBD); currently random
        if self.action_type == None:
            self.action_type = random.choice(self.full_action_list)

            if self.action_type == self.move_list:
                self.filter_moves(world, sim_params)
                self.sub_action = random.choice(self.filtered_move_list)
                self.sub_action(sim_params)
                # after running sub act, reset both to None
                self.action_type = None
                self.sub_action = None
            elif self.action_type == self.resource_actions:
                self.sub_action = random.choice(self.action_type)
                self.sub_action(self, round_num, world, sim_params)

        # if agent was already in reso action ...
        elif self.action_type == self.resource_actions:
            self.sub_action = random.choice(self.action_type)
            self.sub_action(self, round_num, world, sim_params)
    
