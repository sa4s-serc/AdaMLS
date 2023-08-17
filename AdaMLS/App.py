import argparse
import io
import csv
from PIL import Image
import argparse
import time
import numpy as np
from fastapi import FastAPI, File, UploadFile
import uvicorn
import os


# rest of the script

app = FastAPI()
input_rate = 0
start_time = 0
total_in = 0

DETECTION_URL = '/v1/object-detection'

@app.post(DETECTION_URL)
async def predict( image: UploadFile = File(...) ):
    global start_time
    global input_rate
    global total_in

    if(time.time() - start_time > 1 ):
            f = open("monitor.csv", "w")
            f.write(f'{input_rate}')
            f.close()
            start_time = time.time()
            input_rate = 0

    input_rate+=1
    im_bytes = await image.read()
    x = time.time()
    filename = f"images/queue{total_in}.csv"

    f = open(filename, "w")
    writer = csv.writer(f)
    writer.writerow([x])
    writer.writerow(im_bytes)
    f.close()
    
    total_in += 1
    return 
    

if __name__ == '__main__':

    port = 5000
    parser = argparse.ArgumentParser(description='Flask API exposing YOLOv5 model')
    parser.add_argument('--port', default=port, type=int, help='port number')
    parser.add_argument('--model', nargs='+', default=['yolov5n'], help='model(s) to run, i.e. --model yolov5n yolov5s')
    opt = parser.parse_args()
    current_model = opt.model[0]  # use the first model in the list as the default
    uvicorn.run(app, host='0.0.0.0', port=opt.port)
    # app.run(host='0.0.0.0', port=opt.port)
