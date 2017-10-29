import random
import time

class Agent():
    """ Macro-Cognitive Agent definition
        Will have several paramters affecting performance:
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

    #!! agent move defintiions
    # note that world wraps around on both axes
    def move_left(self, sim_params):
        if self.x - 1 >= 0:
            self.x -= 1
        else:
            self.x = sim_params.world_size - 1

    def move_right(self, sim_params):
        if self.x + 1 <= sim_params.world_size - 1:
            self.x += 1
        else:
            self.x = 0

    def move_down(self, sim_params):
        if self.y - 1 >= 0:
            self.y -= 1
        else:
            self.y = sim_params.world_size - 1

    def move_up(self, sim_params):
        if self.y + 1 <= sim_params.world_size - 1:
            self.y += 1
        else:
            self.y = 0

    def find_targets(self, world, sim_params):
        # find squares adjacent to agent
        # check up square
        if self.y == sim_params.world_size-1:
            up_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == 0), None)
        else:
            up_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == self.y + 1), None)

        # check down square
        if self.y == 0:
            down_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == sim_params.world_size-1), None)
        else:
            down_target = next((square for square in world.squares if square.x ==\
            self.x and square.y == self.y - 1), None)

        # check right square
        if self.x == sim_params.world_size-1:
            right_target = next((square for square in world.squares if\
            square.x == 0 and square.y == self.y), None)
        else:
            right_target = next((square for square in world.squares if square.x ==\
            self.x + 1 and square.y == self.y), None)

        # check left square
        if self.x == 0:
            left_target = next((square for square in world.squares if square.x ==\
            sim_params.world_size-1 and square.y == self.y), None)
        else:
            left_target = next((square for square in world.squares if square.x ==\
            self.x - 1  and square.y == self.y), None)
     
        return(up_target, down_target, right_target, left_target)

    def filter_move_actns(self, world, sim_params):
        # two agents cannot occupy the same point in space
        # check which moves are allowable before choosing one
        # this is based on which adjacent squares are occupied
        # find_targets will grab surrounding squares
        up_target, down_target, right_target, left_target = \
                self.find_targets(world, sim_params)

        # append moves to filtered_move list
        if not up_target.occupied:
            self.filtered_move_list.append(self.move_up)
        if not down_target.occupied:
            self.filtered_move_list.append(self.move_down)
        if not right_target.occupied:
            self.filtered_move_list.append(self.move_right)
        if not left_target.occupied:
            self.filtered_move_list.append(self.move_left)

    # def filter_reso_actns(self, world, sim_params)

    #!! agent resource action definitions
    def harvest(self, round_num, world, sim_params):
        # if agent has already started a harvest
        if self.action_end_time != None:
            # check if harvest is finished
            if round_num > self.action_end_time:
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
                # self.filtered_move_list = []
        
            # if agent hasn't finished req'd num of harvest rounds ...
            # don't change action yet
            else:
                pass

        #if agent hasn't started harvest, check if resource present
        else:
            if self.position.square_resource:
                self.action_start_time = round_num
                self.action_end_time = round_num + self.harvest_duration

            # if agent attempts to harvest, but no reso present ...
            # turn is basically wasted
            else:
                self.action_type = None
        # end harvest() definition 

    def refine(self, sim_params, resource):
        pass

    def trade(self, world):
        up_target, down_target, right_target, left_target = \
                self.find_targets(world, sim_params)
        targets = [up_target, down_target, right_target, left_target]
        trade_targets = [target for target in targets if target.occupied]
        print("possible targets:")
        print(targets)
        time.sleep(3)

    # move_list defines how agents can move around the map
    # multiple agents cannot occupy the same square
    move_list = [move_left, move_right, move_down, move_up]

    # resource_actions defines what agents can do with resources
    # by default, only can harvest
    # add trade if other agents are adjacent,
    # add refine if agent possesses a reso
    resource_actions = [harvest]

    # skills will be a combination of a transform and a speed
    # This might involve interaction with memory...
    # skills = {}

    # full action list is a combination of all possible actions
    full_action_list = [move_list, resource_actions]

    # print agent position to screen
    def print_position(self):
      print("Agent ", self.id, " position x,y:", self.x, self.y)
      pass

    def act(self, world, round_num, sim_params):
        # filtered move list is built based on which adjacent squares are empty
        # it is rebuilt on each turn
        self.filtered_move_list = []
        self.position = next((square for square in world.squares \
            if square.x == self.x and square.y == self.y), None)
        # self.print_position()

        # grab agent's current square from world.squares
        # "next" grabs matching instance from iterator
        # self.position = next((square for square in world.squares \
        #     if square.x == self.x and square.y == self.y), None)

        # if agent currently not doing anything ...
        # self.action_type: choose between moving, manipulating resources,
        # or something else (TBD); currently random
        if self.action_type == None:
            self.action_type = random.choice(self.full_action_list)

            # 1. if agents selects a move actn ...
            if self.action_type == self.move_list:
                # filter to moves to only those that lead to unoccupied squares
                self.filter_move_actns(world, sim_params)
                # choose from subset of filtered moves
                if len(self.filtered_move_list) == 0:
                    pass
                else:
                    # set current square to unoccupied
                    self.position.occupied = False

                    self.sub_action = random.choice(self.filtered_move_list)
                    # sim params passed to movement, for dimensions of world
                    self.sub_action(sim_params)

                # after running sub act, reset both to None
                self.action_type = None
                self.sub_action = None
                # grab new position and set square.occupied
                self.position = next((square for square in world.squares \
                    if square.x == self.x and square.y == self.y), None)
                self.position.occupied = True

            # 2. if agent selects a reso action ...
            elif self.action_type == self.resource_actions:
                # start new reso action
                # # filter reso actions based on whether agent holds resos
                # if self.inventory not None:
                #     self.filtered_reso_action
                self.sub_action = random.choice(self.action_type)
                self.sub_action(self, round_num, world, sim_params)

        # if agent was already in reso action, continue
        # could DRY up, duplicates call above
        elif self.action_type == self.resource_actions:
            self.sub_action = random.choice(self.action_type)
            self.sub_action(self, round_num, world, sim_params)
    
