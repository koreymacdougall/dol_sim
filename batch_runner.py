from runner import round_runner
# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# world_sizes = []
# num_agents = []
# round_lengths =[]
num_runs_per_condition = 10000
# num_agents = [1,2,3,4,5,6]
num_agents = list(range(1, 26, 2))

total_rounds_to_run = num_runs_per_condition*len(num_agents)
current_run_num = 0
print("Running ", total_rounds_to_run, " rounds")

# initial header setup
with open ("data/data_test.txt", "w") as f:
    f.write("RunNumTot, RunNumCond, NumRunsCompletion, NumAgents, InitResoCnt \n")

#run a single iteration of the sim
for n_agents in num_agents:
    for run_num_in_cond in range(num_runs_per_condition):
        print("Running round: ", current_run_num, " of", total_rounds_to_run, " total rounds")
        current_run_num += 1
        num_rounds_to_complete, raw_resos = round_runner(n_agents)
        with open ("data/data_test.txt", "a") as f:
            f.write("{}, {}, {}, {}, {}  \n".format( \
                current_run_num, \
                run_num_in_cond, \
                num_rounds_to_complete, \
                n_agents, \
                raw_resos ))

with open ("data/data_test.txt", "r") as f:
    #print(f.read(), end="")
    pass
