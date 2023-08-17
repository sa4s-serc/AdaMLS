# naive
import requests
from Analyzer import Analyzer
import time
import pandas as pd
import os


def get_pending_images_count():
    image_folder = 'images'  # specify the path to your images folder
    return len(os.listdir(image_folder))


def get_past_50_rows_average():

    # log file.
    log_file = "log.csv"

    # Read the log file and get the last 50 rows
    df = pd.read_csv(log_file, header=None)
    last_50_rows = df.tail(30)

    # Define column numbers for each value of interest
    col_avg_confidence = 1
    col_response_time = 5
    col_detection_boxes = 4

    # Calculate the average of each column of interest
    avg_confidence = last_50_rows[col_avg_confidence].mean()
    avg_response_time = last_50_rows[col_response_time].mean()
    avg_detection_boxes = last_50_rows[col_detection_boxes].mean()

    # Return the average values as a list
    return [avg_confidence, avg_response_time, avg_detection_boxes]


analyzer_obj = Analyzer()


class Monitor():

    def continous_monitoring(self):
        monitor_dict = {}
        print("Running the adaptation effector module")
        st = time.time()
        while (1):

            if (time.time() - st > 1):

                # get the average of past 50 logged data
                last_50 = get_past_50_rows_average()

                # retriev the input rate from monitor.csv file
                df = pd.read_csv('monitor.csv', header=None)

                if df.empty == True:
                    time.sleep(0.1)
                    continue

                array = df.to_numpy()
                monitor_dict["input_rate"] = array[0][0]

                # retriev current model from model.csv file
                df = pd.read_csv('model.csv', header=None)
                array = df.to_numpy()
                model_name = array[0][0]
                monitor_dict["model"] = model_name

                monitor_dict["last_50"] = last_50
                monitor_dict["pending_images"] = get_pending_images_count()

                if (model_name != 'yolov5n' and model_name != 'yolov5s' and model_name != 'yolov5l' and model_name != 'yolov5m' and model_name != 'yolov5x'):
                    continue

                print(monitor_dict)

                # sends data to analyzer to perform data analysis.
                analyzer_obj.perform_analysis(monitor_dict)
                st = time.time()


if __name__ == '__main__':
    monitor_obj = Monitor()
    monitor_obj.continous_monitoring()
