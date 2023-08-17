#to start the API endpoint
python3 App.py

#to run Request_send.py file.
locust -f Request_send.py --host=http://localhost:5000/v1

#to run process.py
python3 process.py

#to run monitor.py
python3 monitor.py
