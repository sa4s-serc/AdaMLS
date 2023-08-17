# AdaMLs - Towards Self-Adaptive Machine Learning-Enabled Systems Through QoS-Aware Model Switching

AdaMLS approach is showcased through an object detection system, a well-established ML use case over the last two decades. The system operates as a `web service` with REST API interface, `model_repo` serving as the ML model repository, a `message_broker` for image streaming, and an `obj_model` using the YOLO algorithm for object detection to process the requests. Together, these components ensure precise and efficient object detection services.

## Initial Set-up:
- Clone the repository using git clone command
- Create an folder named `IMAGES` containing all the test image files in both the `NAVIE` and `AdaMLS` directories.
- Create another empty folder named `images` in both the `NAVIE` and `AdaMLS` directories. This folder is used to store the image data present in the queue.
- Run command: `pip install --upgrade ultralytics`

## Learning Engine 

1. Learning Engine  uses COCO Test dataset 2017, to test all yolov5 model's indiviusaly and get detection resutls of each model for clustering.
2. `1_Optimal_K_Values.ipynb` file in side `Learning Engine and Adaptation Rules` directory determines optimal number's of cluster for each model.
3. `2_Clustering_Rules.ipynb` file in side `Learning Engine and Adaptation Rules` directory generates C.I metrics (table) for each model which will act as adaptaion rules for AdaMLS approch.

## Runing Object-detection prototype
**Note:** 
1. Empty the images folder before starting the prototype
2. Clear/ Delete the log.csv file before each run.

### Image Processing:
Prior to users initiating their requests, it is necessary to execute a program that handles the processing of input images.

1.Runing single state of the art Yolov5 models:
- This includes: `yolov5n`, `yolov5s`, `yolov5m`, `yolov5l`, `yolov5x` models

| Model                                                                                           | size<br><sup>(pixels) | mAP<sup>val<br>50-95 | mAP<sup>val<br>50 | Speed<br><sup>CPU b1<br>(ms) | Speed<br><sup>V100 b1<br>(ms) | Speed<br><sup>V100 b32<br>(ms) | params<br><sup>(M) | FLOPs<br><sup>@640 (B) |
| ----------------------------------------------------------------------------------------------- | --------------------- | -------------------- | ----------------- | ---------------------------- | ----------------------------- | ------------------------------ | ------------------ | ---------------------- |
| [YOLOv5n](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt)              | 640                   | 28.0                 | 45.7              | **45**                       | **6.3**                       | **0.6**                        | **1.9**            | **4.5**                |
| [YOLOv5s](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt)              | 640                   | 37.4                 | 56.8              | 98                           | 6.4                           | 0.9                            | 7.2                | 16.5                   |
| [YOLOv5m](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m.pt)              | 640                   | 45.4                 | 64.1              | 224                          | 8.2                           | 1.7                            | 21.2               | 49.0                   |
| [YOLOv5l](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l.pt)              | 640                   | 49.0                 | 67.3              | 430                          | 10.1                          | 2.7                            | 46.5               | 109.1                  |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x.pt)              | 640                   | 50.7                 | 68.9              | 766                          | 12.1                          | 4.8                            | 86.7               | 205.7                  |

- To specicify model you want to run paste its name in model.csv file present in NAVIE directory
- From the NAVIE directory run script process.py file using command: `python3 process.py`   

2.Running the NAVIE approch:
- From the NAVIE directory run script process.py file using command: `python3 process.py`   

3.Running the AdaMLS approch:
-- From the AdaMLS directory run script process.py file using command: `python3 process.py`   

### API Setup:
To facilitate user interaction and provide a seamless experience, an API is initiated

1.Runing single state of the art Yolov5 models:
- From the NAVIE directory run the script App.py using command: `python3 App.py`

2.Running the NAVIE approch:
- From the NAVIE directory run the script App.py using command: `python3 App.py`   

3.Running the AdaMLS approch:
- From the AdaMLS directory run the script App.py using command: `python3 App.py`  

### Sending Requests:
In order to simulate a FIFA98 scenario with up to 28 parallel requests per second and a total of 25,000 requests, images from the "IMAGES" folder will be sent at a rate that adheres to the resampled scaled inter-arrivals specified in the "resampled_scaled_inter_arrivals.csv" file.

1.Runing single state of the art Yolov5 models:
- From the NAVIE directory run the script App.py using command: `locust -f Request_send.py --host=http://localhost:5000/v1`

2.Running the NAVIE approch:
- From the NAVIE directory run the script App.py using command: `locust -f Request_send.py --host=http://localhost:5000/v1`   

3.Running the AdaMLS approch:
- From the AdaMLS directory run the script App.py using command: `locust -f Request_send.py --host=http://localhost:5000/v1` 

After running the above command, go to the URL http://0.0.0.0:8089 and click `Start swarming`
  
### Running MAPE-K loop:
To facilitate the process of adaptation we run a MAPE-K loop. This loop involves continuously monitoring various metrics, analyzing the received data, formulating a plan based on the analysis, and finally executing the corresponding actions outlined in the plan.

1.Runing single state of the art Yolov5 models:
- Since the system is running a single model continuously, there is no need for the MAPE-K loop as it is not required to monitor, analyze, plan, and execute actions for adaptation.

2.Running the NAVIE approch:
- From the NAVIE directory run the script monitor.py using command: `python3 monitor.py`   

3.Running the AdaMLS approch:
- From the AdaMLS directory run the script App.py using command: `python3 monitor.py` 

## Result's
1. We have conducted are experiment on randomly selected 25,000 images from [COCO2017 unlabeled dataset](https://cocodataset.org/#download)
2. We have simulated [FIFA98](https://ita.ee.lbl.gov/html/contrib/WorldCup.html) scenario of up to 28 parallel requests/sec and 25,000 total requests.
3. Our experimental log's can be found in Results directory:
- For NAVIE approch: `NAVIE_log.csv`
- For AdaMLS approch: `AdaMLS_log.csv` 
- For YOLOV5n model: `Nano_log.csv`
- For YOLOV5s model: `Small_log.csv`
- For YOLOV5m model: `Medium_log.csv`
- For YOLOV5l model: `Large_log.csv`
- For YOLOV5x model: `Xlarge_log.csv`

#### For AdaMLS, in the figure below, demonstrates an increase in total utility for equal weights on response time and confidence score by up to 39\% compared with Yolov5n as the second-best.
![Utility](https://github.com/karthikv1392/ArchML/blob/main/Results/Utility.png)

#### In terms of efficiency, AdaMLS incurs more model switch instances (308 vs 49), as illustrated in figure below:
![Switching](https://github.com/Arya-Ayra/AdaMLS/blob/main/Results/Switching.png)

