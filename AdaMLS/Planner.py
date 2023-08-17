from Execute import Executor
import pandas as pd

class Planner():
    def __init__(self,  input_rate , model, cluster ):
        self.input_rate = input_rate
        self.model = model
        self.cluster = cluster
        print("Planner object created")

    def generate_adaptation_plan(self , count):
        
        action = 0
        file_name = f"Knowledge_get_cluster/{self.model}_get_cluster.csv"
        df = pd.read_csv(file_name)
        array = df.to_numpy()

        no_of_row = len(array)
        row_num = -1
        for i in range(no_of_row):
            if( array[i][0] == self.cluster):
                row_num = i
                break

        col_list = [2,11,19,27,35]
        possible = []
        for i in col_list:
            res_time = array[row_num][i]
            rate_col = 1/res_time
            if(rate_col >=self.input_rate):
                possible.append(df.columns[i])
        
        if(len(possible) == 0):
            print("In Planner but suggested no adaptation")
            action = 1
            exe_obj = Executor()
            exe_obj.perform_action(action)
            return

        models_possible =[]

        for name in possible :
            if(name == 'Response Time(s)_CI_Lower'):
                models_possible.append('')
            elif(name == 'Response Time(s)_large_CI_Lower'):
                models_possible.append('large')
            elif(name == 'Response Time(s)_xlarge_CI_Lower'):
                models_possible.append('xlarge')
            elif(name == 'Response Time(s)_medium_CI_Lower'):
                models_possible.append('medium')
            elif(name == 'Response Time(s)_nano_CI_Lower'):
                models_possible.append('nano')
            elif(name == 'Response Time(s)_small_CI_Lower'):
                models_possible.append('small')
        
        print(models_possible)

        conf_col_name = []
        for model in models_possible:
            if model != "":
                conf_col_name.append( f'Avg. Confidence_{model}_CI_Lower' )
            else:
                conf_col_name.append( f'Avg. Confidence_CI_Lower' )
        
        

        model = ''
        maxx = -1
        for conf_name in conf_col_name:
            conf = df.loc[row_num][conf_name]
            if(maxx < conf):
                maxx = conf
                pos = conf_col_name.index(conf_name)

                model = models_possible[pos]
               
        if model == "":
            return
                
        if( model == 'nano'):
            action = 1
        elif( model == "small" ):
            action = 2
        elif( model == 'medium' ):
            action = 3
        elif( model == 'large' ):
            action = 4  
        elif( model == 'xlarge' ):
            action = 5
        else:
            print("In Planner but suggested no adaptation")
            action = 1
            
        #creates Executor object and call's to perform action.
        exe_obj = Executor()
        exe_obj.perform_action(action)