import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa
import random

from Agent import Agent
from sumo_utils import run_episode
from gen_sim import gen_sim

NUM_EPISODES = 2  # Number of complete simulation runs
COMPETITION_ROUND = 1  # 1 or 2, depending on which competition round you are in
random.seed(COMPETITION_ROUND)

"""
state = [curr_open_dir, 8*detector(waiting times)]
Where:
- detector[i]: Waiting time for the vehicle on detector[i] since it was last moving with speed > 0.1 ms^{-1}
- detector[i] for i in [0-3] is near traffic light
- detector[i] for i in [4-7] is far from traffic light 
- For illustration of detector positions and numbering (check attached sensor_data.png)
----------------------------------------------------------------------------------------
- curr_open_dir for COMPETITION_ROUND 1: (0 for vertical, 1 for horizontal) --> possible actions (0, 1)
"""

if __name__ == "__main__":

    print('Starting Sumo...')
    # The normal way to start sumo on the CLI
    sumoBinary = checkBinary('sumo')
    # comment the line above and uncomment the following one to instantiate the simulation with the GUI

    # sumoBinary = checkBinary('sumo-gui')

    agent = Agent()  # Instantiate your agent object
    waiting_time_per_episode = []  # A list to hold the average waiting time per vehicle returned from every episode

    for e in range(NUM_EPISODES):
        # Generate an episode with the specified probabilities for lanes in the intersection
        # Returns the number of vehicles that will be generated in the episode
        vehicles = gen_sim('', round=COMPETITION_ROUND,
                           p_west_east=0.3, p_east_west=0.2,
                           p_north_south=0.2, p_south_north=0.1)

        print('Starting Episode ' + str(e) + '...')

        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
        traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                     "--time-to-teleport", "-1",
                     "--tripinfo-output", "tripinfo.xml", '--start', '-Q'], label='contestant')
        # Connection to simulation environment
        conn = traci.getConnection("contestant")
        # Run a complete simulation episode with the agent taking actions for as long as the episode lasts.
        # An episode lasts as long as there are cars in the simulation AND the time passed < 1000 seconds
        total_waiting_time, waiting_times, total_emissions = run_episode(conn, agent, COMPETITION_ROUND)
        # Cleaning up TraCi environments
        traci.switch("contestant")
        traci.close()
        # Calculate the avg waiting time per vehicle
        avg_waiting_time = total_waiting_time / vehicles
        avg_emissions = total_emissions / (1000 * vehicles)
        waiting_time_per_episode.append(avg_waiting_time)

        print('episode[' + str(e) + '] Average waiting time = ' + str(avg_waiting_time)
              + ' (s) -- Average Emissions (CO2) = ' + str(avg_emissions) + "(g)")
