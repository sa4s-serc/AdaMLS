#determine if the systems needs adaption. Checks if the parameters/ thresholds
#are been crosed ...........
from Planner import Planner
import pandas as pd
import time
import numpy as np
import os


def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def find_closest_cluster(point, cluster_data, columns):
    min_distance = float('inf')
    closest_cluster = None

    for _, row in cluster_data.iterrows():
        ci_lower = row[[f"{col}_CI_Lower" for col in columns]].values
        ci_upper = row[[f"{col}_CI_Upper" for col in columns]].values

        distance_lower = euclidean_distance(point, ci_lower)
        distance_upper = euclidean_distance(point, ci_upper)

        min_distance_row = min(distance_lower, distance_upper)

        if min_distance_row < min_distance:
            min_distance = min_distance_row
            closest_cluster = row['SKMeans_Cluster']

    return closest_cluster

def find_cluster(last_50, model):
    file_name = f"Knowledge_get_cluster/{model}_get_cluster.csv"

    input_files = [file_name]
    categories = ['Avg. Confidence', 'Response Time(s)', 'Detection boxes']

    for input_file in input_files:
        df = pd.read_csv(input_file)

        # Calculate variance for each CI category
        variances = {}
        for col in categories:
            lower_var = df[f"{col}_CI_Lower"].var()
            upper_var = df[f"{col}_CI_Upper"].var()
            variances[col] = lower_var + upper_var

        # Select the two categories with the highest variance
        highest_variance_categories = sorted(variances, key=variances.get, reverse=True)[:2]
        print(f"Highest variance categories Xlarge: {highest_variance_categories}")

        col1 = categories.index(highest_variance_categories[0])
        col2 = categories.index(highest_variance_categories[1])
                        
        # Create a new CSV file containing only the cluster number and the CI columns for the selected categories
        mapping_columns = ['SKMeans_Cluster'] + [f"{col}_CI_Lower" for col in highest_variance_categories] + [f"{col}_CI_Upper" for col in highest_variance_categories]
        mapping_df = df[mapping_columns]
        mapping_file = os.path.splitext(input_file)[0] + "_mapping.csv"
        mapping_df.to_csv(mapping_file, index=False)

        # Find the closest cluster for a given point
        point = np.array([last_50[col1], last_50[col2]])  # Example point with values for the two categories with the highest variance
        closest_cluster = find_closest_cluster(point, mapping_df, highest_variance_categories)
        print(f"Closest cluster for point {point} and categories {highest_variance_categories}: {closest_cluster}")
        print(f"Closest cluster for point {point}: {closest_cluster}")
        return closest_cluster

def get_max_min(cluster,model):
    file_name = f"Knowledge_get_cluster/{model}_get_cluster.csv"

    df = pd.read_csv(file_name)
    array = df.to_numpy()

    no_of_row = len(array)
    row_num = -1
    for i in range(no_of_row):
        if( array[i][0] == cluster):
            row_num = i
            break
    
    min_res_time = array[row_num][2]
    max_res_time = array[row_num][6]

    max_rate = 1/min_res_time
    min_rate = 1/max_res_time
    
    return [min_rate, max_rate]

    
class Analyzer():
    def __init__(self):
        
        self.time = -1
        self.count = 0


    def perform_analysis(self,monitor_dict):
        print("Inside the Analyzer: Performing the analysis")
        
        model = monitor_dict["model"]

        closest_cluster = find_cluster(monitor_dict["last_50"] , model)

        input_rate = monitor_dict["input_rate"]
        pending_images = monitor_dict["pending_images"]
        range = get_max_min(closest_cluster,model)

        excess_images = max(0, pending_images - range[1])

        # Calculate the adjusted input rate
        adjusted_input_rate = input_rate + excess_images
        current_time = time.time()

        if ((adjusted_input_rate >= range[0] and adjusted_input_rate <= range[1]) == False):
            if self.time == -1:
                self.time = current_time
            # if threshold sre violated for more than 0.25 sec, we create planner object to obtain the adaptation plan
            elif current_time - self.time > 0.25:
                # initialize plan_obj....
                self.count += 1
                print("Creating planner object: ")
                plan_obj = Planner(adjusted_input_rate, model, closest_cluster)
                plan_obj.generate_adaptation_plan(self.count)
        else:
            self.time = -1