from runner import round_runner
# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# world_sizes = []
# num_agents = []
# round_lengths =[]
num_runs = 500
num_agents = [1,2,3, 4, 5, 6]

# initial header setup
with open ("data/data_test.txt", "a") as f:
    f.write("Run Num, Num Runs to Completion, Num Agents, \n")

for agent_count in num_agents:
    for run in range(num_runs):
        num_rounds_to_complete = round_runner(agent_count)
        with open ("data/data_test.txt", "a") as f:
            f.write("{}, {}, {},  \n".format(run, num_rounds_to_complete, \
                agent_count ))

with open ("data/data_test.txt", "r") as f:
    #print(f.read(), end="")
    pass
