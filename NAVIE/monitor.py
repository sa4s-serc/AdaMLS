# naive
import requests
from Analyzer import Analyzer
import time
import pandas as pd


analyzer_obj = Analyzer()


class Monitor():
    def continous_monitoring(self):
        monitor_dict = {}

        # indicates monitoring has started
        print("Running the adaptation effector module")
        st = time.time()
        while (1):

            # we monitor every 1 second.
            if (time.time() - st > 1):

                # retriev the input rate from monitor.csv file
                df = pd.read_csv('monitor.csv', header=None)
                array = df.to_numpy()

                monitor_dict["input_rate"] = array[0][0]

                # retriev current model from model.csv file
                df = pd.read_csv('model.csv', header=None)

                array = df.to_numpy()
                model_name = array[0][0]
                monitor_dict["model"] = model_name

                if (model_name != 'yolov5n' and model_name != 'yolov5s' and model_name != 'yolov5l' and model_name != 'yolov5m' and model_name != 'yolov5x'):
                    continue

                print(monitor_dict)

                # sends data to analyzer to perform data analysis.
                analyzer_obj.perform_analysis(monitor_dict)
                st = time.time()


if __name__ == '__main__':
    monitor_obj = Monitor()
    monitor_obj.continous_monitoring()
