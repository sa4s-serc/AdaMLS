import csv
import io
import csv
from PIL import Image
import time
import torch
import psutil
import pandas as pd
import imghdr
import os

models = {}
total_processed = 0
global_start_time = 0


def get_current():
    df = pd.read_csv('model.csv', header=None)
    array = df.to_numpy()
    print(array[0][0])
    return array[0][0]


def process_row(im_bytes, start_time):

    # run's the object detection on the received data

    global total_processed
    global global_start_time

    image_format = imghdr.what(None, h=im_bytes)
    if image_format is None:
        return
    current_model = get_current()
    if current_model in models:
        try:
            if (total_processed == 0):
                global_start_time = time.time()

            im = Image.open(io.BytesIO(im_bytes))
            current_time = time.time()
            results = models[current_model](im)

            current_cpu = psutil.cpu_percent(interval=None)
            total_processed += 1

            detection = results.pandas().xyxy[0]
            confidences = detection['confidence'].tolist()
            current_conf = sum(confidences)
            current_boxes = len(confidences)

            if (current_boxes != 0):
                avg_conf = current_conf/current_boxes

            else:
                avg_conf = 0

            t = time.time()
            current_time = t - current_time
            start_time = t - start_time
            absolute_time = t - global_start_time

            # writes the logs in a log.csv file.
            print("To write in log file.\n")
            f = open("log.csv", "a")
            f.write(
                f'{total_processed},{avg_conf},{current_model},{current_cpu},{current_boxes},{current_time},{start_time},{absolute_time}\n')
            f.close()

            return detection.to_json(orient='records')
        except Exception as e:
            print(str(e))
            return {'error': str(e)}
    else:
        return {'error': f'Model {current_model} not found'}


def start_processing():

    # checks for the current image csv file in images folder, and if it exists, it sends the image_data to process_row function

    global total_processed
    while True:
        r = 0
        image_path = f"images/queue{total_processed}.csv"
        image_path_next = f"images/queue{total_processed+1}.csv"

        if os.path.exists(image_path) == False:
            print(f"File not exist {total_processed}")

            if (os.path.exists(image_path_next) == False):
                time.sleep(0.03)
                continue
            else:
                print("Skipping file...........................")
                total_processed += 1
                image_path = image_path_next

        with open(image_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) >= 2:
            try:
                first_row = rows[1]
                start_time = float(rows[0][0])
                print(start_time)
                first_row = [int(x) for x in first_row]
                first_row = bytes(first_row)

                # Process the first row
                process_row(first_row, start_time)
                # Delete the first row from the CSV file
                os.remove(image_path)
                # Do something with the processed row
                print("Finished processing")

            except Exception as e:
                print("Inside exception")
                print("skipping file--------------------------------")
                total_processed += 1

        elif len(rows) == 1:
            print("skipping file----------------------------------")
            total_processed += 1
        else:
            print("Empty")
            time.sleep(0.5)
            continue


if __name__ == '__main__':

    # loads all 5 models at the start in an array named models

    for m in {'yolov5n', 'yolov5s', 'yolov5m', 'yolov5l', 'yolov5x'}:
        models[m] = torch.hub.load(
            'ultralytics/yolov5', m, force_reload=True, skip_validation=True)

    # start processing the images.
    start_processing()
