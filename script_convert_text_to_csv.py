import numpy as np 
import pandas as pd 
name_store_excel = 'sensors_mgb.csv'
path_dir  = "test_second_gearbox.txt"

total_data_set = {
    'time':[],
    's1'  :[],
    's2'  :[],
    's3'  :[],
    's4'  :[],
    's5'  :[],
    's6'  :[] 
}

with open(path_dir,'r') as file:
    for line in file.readlines():
        print(" ******** ****** start reading ****** ******* ")
        t1,s1,s2,s3,s4,s5,s6 = line.split(',')
        s6 = s6.strip()
        total_data_set['time'].append(t1)
        total_data_set['s1'].append(s1)
        total_data_set['s2'].append(s2)
        total_data_set['s3'].append(s3)
        total_data_set['s4'].append(s4)
        total_data_set['s5'].append(s5)
        total_data_set['s6'].append(s6)
        print(" ******** ****** finish reading ****** ******* ")

df = pd.DataFrame(total_data_set)
df.to_csv(name_store_excel,index=False)


    
        




