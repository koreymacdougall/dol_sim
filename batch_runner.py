from runner import single_run_runner
# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# rounds_per_run =[]
num_runs_per_condition = 2
num_agents = [3,5]
world_size = [5, 9]

#TODO - variabalize this
total_runs = num_runs_per_condition*len(num_agents)*len(world_size)
current_run_num = 1
print("Running ", total_runs, " rounds")

# initial header setup
with open ("data/data_test.txt", "w") as f:
    f.write("RunNumTot, RunNumOfCond, NumRoundsToCompletion, NumAgents,\
            InitResoCnt, HarvestedResos \n")

# run a single iteration of the sim
# TODO - make these nested for loops cleaner
for w_size in world_size:
    for n_agents in num_agents:
        for run_num_in_cond in range(num_runs_per_condition):
            print("Run: ", current_run_num, " of", total_runs, " total runs")
            num_rounds_to_completion, raw_resos, harv_resos =\
            single_run_runner(n_agents, w_size)
            with open ("data/data_test.txt", "a") as f:
                f.write("{}, {}, {}, {}, {}, {} \n".format( \
                    current_run_num, \
                    run_num_in_cond + 1, \
                    num_rounds_to_completion, \
                    n_agents, \
                    raw_resos,\
                    harv_resos))
            current_run_num += 1

with open ("data/data_test.txt", "r") as f:
    #print(f.read(), end="")
    pass
