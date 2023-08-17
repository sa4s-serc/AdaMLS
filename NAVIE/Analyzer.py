# determine if the systems needs adaption. Checks if the parameters/ thresholds are violated
from Planner import Planner
import pandas as pd
import time


class Analyzer():
    def __init__(self):

        # setting threshold values obtained from knowledge.csv file.

        self.time = -1

        df = pd.read_csv('knowledge.csv', header=None)

        array = df.to_numpy()
        self.thresholds = {}

        self.thresholds["yolov5n_rate_min"] = array[0][1]
        self.thresholds["yolov5n_rate_max"] = array[0][2]

        self.thresholds["yolov5s_rate_min"] = array[1][1]
        self.thresholds["yolov5s_rate_max"] = array[1][2]

        self.thresholds["yolov5m_rate_min"] = array[2][1]
        self.thresholds["yolov5m_rate_max"] = array[2][2]

        self.thresholds["yolov5l_rate_min"] = array[3][1]
        self.thresholds["yolov5l_rate_max"] = array[3][2]

        self.thresholds["yolov5x_rate_min"] = array[4][1]
        self.thresholds["yolov5x_rate_max"] = array[4][2]

        self.count = 0

    def perform_analysis(self, monitor_dict):

        print("Inside the Analyzer: Performing the analysis")

        input_rate = monitor_dict["input_rate"]
        model = monitor_dict["model"]

        str_min = model + "_rate_min"
        str_max = model + "_rate_max"
        current_time = time.time()

        # get's the minimum and maximum threshold values for the current working model.

        min_val = self.thresholds.get(str_min)
        max_val = self.thresholds.get(str_max)

        if ((max_val >= input_rate and min_val <= input_rate) == False):

            if (self.time == -1):
                self.time = current_time
            # if threshold sre violated for more than 0.25 sec, we create planner object to obtain the adaptation plan
            elif (current_time - self.time > 0.25):

                self.count += 1
                print("Creating planner object: ")
                plan_obj = Planner(input_rate, model)
                plan_obj.generate_adaptation_plan(self.count)

        else:
            self.time = -1
