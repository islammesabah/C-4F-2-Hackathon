import random
from sklearn.linear_model import Perceptron
import pickle
import numpy as np
import pandas as pd
import copy

import sumo_utils as su
 
class Agent:
    def __init__(self):
        self.t = 0
        self.prev_action = 0
        self.pref_total_time = 0

    def cost(self,state,conn, vehicle_ids):
        curr_open_dir = su.get_curr_open_dir(conn)
        waiting_count = su.get_waiting_count(conn,vehicle_ids)
        total_waiting_time = su.get_total_waiting_time(conn,vehicle_ids)
        total_co2 = su.get_total_co2(conn,vehicle_ids)
        total_accumulated_waiting_time = su.get_total_accumulated_waiting_time(conn,vehicle_ids)
        total_speed = su.get_total_speed(conn,vehicle_ids)
        moving_count = su.get_moving_count(conn,vehicle_ids)
        self.t = self.t+1

        action = curr_open_dir[0]
        if(self.pref_total_time != 0):
            if(total_waiting_time > self.pref_total_time):
                if(self.t>4):
                    self.t=0
                    action = (self.prev_action+1)%2
            else:
                action = self.prev_action

        
        self.pref_total_time = total_waiting_time
        self.prev_action = action
        
        # print(self.t)
        # if(moving_count < waiting_count):
        #     if(self.t>4):
        #         self.t=0
        #         return (curr_open_dir[0]+1)%2

        return action
        

    def select_action(self, state, conn=None, vehicle_ids=None):
        columns=['direction', 'sens1', 'sens2','sens3','sens4','sens5','sens6','sens7','sens8','action']
        try:
            df = pd.read_csv("dataset/singleIntersectData1.csv")
        except:
            df = pd.DataFrame(columns=columns)
        if(conn) != None:
            y = self.cost(state,conn,vehicle_ids)

            data = np.array([state+[y]])
            df2 = pd.DataFrame(data,columns=columns)
            df = df.append(df2, ignore_index=True)
            df.to_csv("dataset/singleIntersectData1.csv", index=False)
            
            return y

        else:
            filename = "DecisionTreeClassifier9.sav"
            clf = pickle.load(open("models/"+filename, 'rb'))
            x = clf.predict([state])[0]
            return int(x)
                    