from Execute import Executor
import pandas as pd

class Planner():
    def __init__(self,  input_rate , model  ):
        self.input_rate = input_rate
        self.model = model
        print("Planner object created")
      

    def generate_adaptation_plan(self , count):
        
        action = 0
        
        df = pd.read_csv('knowledge.csv', header=None)
        array = df.to_numpy()

        in_rate = self.input_rate

        #check's which model's thershold range is input rate within and accordingly determines the action.

        if( in_rate >= array[0][1] and in_rate <= array[0][2]):
            action = 1
        elif( in_rate >= array[1][1] and in_rate <= array[1][2] ):
            action = 2
        elif( in_rate >= array[2][1] and in_rate <= array[2][2] ):
            action = 3
        elif( in_rate >= array[3][1] and in_rate <= array[3][2] ):
            action = 4
        elif ( in_rate >= array[4][1]  and in_rate <= array[4][2]  ) : #and in_rate < array[4][2]
            action = 5
        else:
            print("In Planner but suggested no adaptation")
            return
        
        #creates Executor object and call's to perform action.
        exe_obj = Executor()
        exe_obj.perform_action(action)