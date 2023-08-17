import requests

class Executor():
 
    def perform_action(self, act):
        print('Inside Execute, performing action: ', act)

        if(act == 1):
            #switch model to n
            print("Switch to n")
          
            f = open("model.csv", "w")
            f.write("yolov5n")
            f.close()

            print("Finished Action 1")

        elif(act == 2):
            #switch model to s
            print("Switch to s")
            f = open("model.csv", "w")
            f.write("yolov5s")
            f.close()
            print("Finished Action 2")

        elif(act == 3):
            #switch model to m
            print("Switch to m")
            f = open("model.csv", "w")
            f.write("yolov5m")
            f.close()
            print("Finished Action 3")

        elif(act == 4):
            #switch model to l
            print("Switch to l")
            f = open("model.csv", "w")
            f.write("yolov5l")
            f.close()
            print("Finished Action 4")
        elif(act == 5):
            print("Switch to x")
            #switch model to l
            f = open("model.csv", "w")
            f.write("yolov5x")
            f.close()

        print("Byeyeyeyeyeye")