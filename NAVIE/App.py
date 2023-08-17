import argparse
import csv
import argparse
import time
from fastapi import FastAPI, File, UploadFile
import uvicorn


#creating a FastAPI endpoint.

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

    if(time.time() - start_time > 1 ):  #measures the input rate of images per second, and writes the rate in monitor.csv file.
            f = open("monitor.csv", "w") #contin's input rate data.
            f.write(f'{input_rate}')
            f.close()
            start_time = time.time()
            input_rate = 0

    input_rate+=1
    im_bytes = await image.read()
    x = time.time()
    filename = f"images/queue{total_in}.csv"# create's a csv file in folder "images"  with name :  queue<request_number>.csv

    f = open(filename, "w")
    writer = csv.writer(f)

    writer.writerow([x]) # 1st  row of this file has the timestamp of the API call
    writer.writerow(im_bytes)# 2nd row stores the current request data

    f.close()
    
    total_in += 1
    return 
    

if __name__ == '__main__':

    port = 5000
    parser = argparse.ArgumentParser(description='Flask API exposing YOLOv5 model')
    parser.add_argument('--port', default=port, type=int, help='port number')
    opt = parser.parse_args()
    uvicorn.run(app, host='0.0.0.0', port=opt.port)
    # app.run(host='0.0.0.0', port=opt.port)