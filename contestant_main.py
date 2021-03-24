import os
import sys
import pandas as pd

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
train = True 
train = False 
NUM_EPISODES = 1 # Number of complete simulation runs
COMPETITION_ROUND = 1  # 1 or 2+, depending on which competition round you are in
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


    x =[19.0 ,11.833333333333334 ,11.608695652173912 ,13.911764705882353 ,15.0 ,14.39622641509434 ,18.174603174603174 ,20.677419354838708 ,9.757575757575758 ,16.363636363636363 ,16.38888888888889 ,12.078947368421053 ,11.233333333333333 ,21.046511627906977 ,17.105263157894736 ,11.121212121212121 ,12.301369863013699 ,16.854166666666668 ,20.134146341463413 ,23.443396226415093 ,24.557377049180328 ,29.65573770491803 ,10.416666666666666 ,11.038461538461538]
    
    agent = Agent()  # Instantiate your agent object
    waiting_time_per_episode = []  # A list to hold the average waiting time per vehicle returned from every episode
    i = 1
    for e in range(NUM_EPISODES):
        # Generate an episode with the specified probabilities for lanes in the intersection
        # Returns the number of vehicles that will be generated in the episode
        # T 1
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=0.3, p_east_west=0.2,
        #                    p_north_south=0.2, p_south_north=0.1)

        # T 2
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=0, p_east_west=2,
        #                    p_north_south=0, p_south_north=2)

        # T 3
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=1, p_east_west=1,
        #                    p_north_south=1, p_south_north=1)

        # T 4
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=0.2, p_east_west=0.4,
        #                    p_north_south=0.4, p_south_north=0.2)

        
        # T 5
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=0.1, p_east_west=0.71,
        #                    p_north_south=0.21, p_south_north=0.81)

        # T 6
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                     # N = 50,
        #                    p_west_east=0, p_east_west=5,
        #                    p_north_south=5, p_south_north=0)
        
        # T 7
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                     # N = 50,
        #                    p_west_east=0, p_east_west=5,
        #                    p_north_south=5, p_south_north=5)
        
        # T 8
        vehicles = gen_sim('', round=COMPETITION_ROUND,
                            # N = 50,
                           p_west_east=5, p_east_west=5,
                           p_north_south=5, p_south_north=0)

        # T 9
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                     # N = 50,
        #                    p_west_east=5, p_east_west=0,
        #                    p_north_south=0, p_south_north=5)

        # T 10       
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                     # N = 50,
        #                    p_west_east=0.1, p_east_west=0,
        #                    p_north_south=0, p_south_north=0.1)

        # T 11
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                     # N = 50,
        #                    p_west_east=0, p_east_west=0.1,
        #                    p_north_south=0.1, p_south_north=0)

        # T 12
        # vehicles = gen_sim('', round=COMPETITION_ROUND,
        #                    p_west_east=0.5, p_east_west=0.5,
        #                    p_north_south=0.5, p_south_north=0.5)

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
        total_waiting_time, waiting_times, total_emissions = run_episode(conn, agent, COMPETITION_ROUND , train = train)
       
        # total_waiting_time, waiting_times, total_emissions = run_episode(conn, agent, COMPETITION_ROUND)
        # Cleaning up TraCi environments
        traci.switch("contestant")
        traci.close()
        # Calculate the avg waiting time per vehicle
        avg_waiting_time = total_waiting_time / vehicles
        avg_emissions = total_emissions / (1000 * vehicles)
        waiting_time_per_episode.append(avg_waiting_time)

        print('episode[' + str(e) + '] Average waiting time = ' + str(avg_waiting_time)
              + ' (s) -- Average Emissions (CO2) = ' + str(avg_emissions) + "(g)")

        if(train):
            i = i+1
            if(i>50):
                df = pd.read_csv("dataset/singleIntersectDataTotalTime.csv")
                df1 = pd.read_csv("dataset/singleIntersectData1.csv")
                df = df.append(df1, ignore_index=True)
                df1.drop(df1.index, inplace=True)
                df.to_csv("dataset/singleIntersectDataTotalTime.csv", index=False)
                df1.to_csv("dataset/singleIntersectData1.csv", index=False)
                i = 0
