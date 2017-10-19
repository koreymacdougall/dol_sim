from runner import round_runner
# TODO - make multiple parameter values, for batch running
# & build batch runner functionality
# world_sizes = []
# num_agents = []
# round_lengths =[]
num_runs = 5
for run in range(num_runs):
    num_rounds_to_complete= round_runner()
    with open ("data/data_test.txt", "a") as f:
        f.write("({!s} round, {!s} num_rounds_to_complete) \n".format(run, num_rounds_to_complete ))

