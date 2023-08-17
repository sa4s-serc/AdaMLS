from locust import HttpUser, task
from gevent import spawn
import csv
import time
import os


class MyUser(HttpUser):
    wait_times = []
    n = 0

    image_data = []
    print(n)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # file containing dat of time interval between 2 consecutive request's
        filename = 'resampled_scaled_inter_arrivals.csv'
        # it is a scaled version of FIFA98 scenario
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            self.wait_times = [float(row[0]) for row in reader]

        self.n = 0

        IMAGES_FOLDER = 'Images'  # Folder with Image's

        for filename in os.listdir(IMAGES_FOLDER):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):

                image_path = os.path.join(IMAGES_FOLDER, filename)

                self.image_data.append(image_path)

    @task
    def my_task(self):

        # read the image file in binary mode.
        image_file = open(self.image_data[self.n], "rb")

        files = {'image': image_file}

        # request being sent to /object-detection API end point.
        spawn(self.client.post, "/object-detection", files=files)
        # print(self.n)

        # sleep for the inter request interval before sending the next API request
        time.sleep(self.wait_times[self.n])

        self.n += 1
