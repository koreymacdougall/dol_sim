from runner import single_run_runner
# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# world_sizes = []
# num_agents = []
# rounds_per_run =[]
num_runs_per_condition = 100
num_agents = [3]
# num_agents = list(range(1, 12, 3))

total_runs = num_runs_per_condition*len(num_agents)
current_run_num = 0
print("Running ", total_runs, " rounds")

# initial header setup
with open ("data/data_test.txt", "w") as f:
    f.write("RunNumTot, RunNumOfCond, NumRoundsToCompletion, NumAgents, InitResoCnt \n")

# run a single iteration of the sim
# TODO - make these nested for loops cleaner
for n_agents in num_agents:
    for run_num_in_cond in range(num_runs_per_condition):
        print("Run: ", current_run_num, " of", total_runs, " total runs")
        current_run_num += 1
        num_rounds_to_completion, raw_resos = single_run_runner(n_agents)
        with open ("data/data_test.txt", "a") as f:
            f.write("{}, {}, {}, {}, {}  \n".format( \
                current_run_num, \
                run_num_in_cond, \
                num_rounds_to_completion, \
                n_agents, \
                raw_resos ))

with open ("data/data_test.txt", "r") as f:
    #print(f.read(), end="")
    pass
