'''
solve pandas error:
    Exception: Data must be 1-dimensional
solution:
    2d-ndarray --> 2d-list
    
'''

import pandas as pd
import numpy as np

l1 = [1,2,3,4]
l2 = [.1,.2,.3,.4]

lists = np.array([l1,l2])
lists = list(lists)
labels = [1,0]

df = pd.DataFrame()
df["list"] = lists
df["label"] = labels

print(df)
###############################################
'''
pandas write csv
'''
import numpy as np
import pandas as pd

data = np.array([i for i in range(10)])
time = np.array([0.1 * i for i in range(10)])
fs = 10

'''
np.savetxt('data.csv', data, delimiter=',')
np.savetxt('time.csv', time, delimiter=',')

filepath = "C:/Users/Brian Hu/Documents/GitHub/eda/temp_folder/pd_read_data/data.csv"
pd_data = pd.read_csv(filepath, skiprows=None, nrows=None)

'''
np.savetxt("table.csv", np.vstack((data,time,fs)).T, delimiter=',', header="data,time,fs", comments="")
filepath = "C:/Users/Brian Hu/Documents/GitHub/eda/temp_folder/pd_read_data/table.csv"

pd_data = pd.read_csv(filepath,skiprows=None,nrows=None)
columns = pd_data.columns
z = pd.Series(pd_data["data"]).to_numpy()