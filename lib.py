import os
import pandas as pd
import  sys
import re

import time

class Canalyse():
    def __init__(self,channel):#channel,bustype):
        self.channel = channel
    def candump(self,filename):
        try:
            os.system('candump -L '+self.channel+' > '+filename)
        except:
            pass
    def canplay(self,filename):
        try:
            os.system('canplayer -I '+filename)
        except:
            pass
    def read(self,filename):
        with open( filename , 'r+' )  as  file:
            log = file.readlines()
            data = pd.DataFrame(columns=['timestamp','channel','id','data'])
            ids = []
            
            for line in log:
                try:
                    res = re.split('#| ',line)
                    res[3] = res[3].strip('\n')
                    if res[3] not in data.loc[data.id == res[2]].data.to_list():
                        data.at[data.shape[0]] = res
                except:
                    pass
      
        return data

    def write(self,df,filename='payload.log'):
        with open(filename,'w+') as file:
            for i in range(df.shape[0]):
                m = [df.loc[i,'timestamp'],df.loc[i,'channel'],df.loc[i,'id']+'#'+df.loc[i,'data']+'\n']
                t = " ".join(m)
                file.write(t)

    def refine(self,source,attack):
        data = pd.DataFrame(columns=['timestamp','channel','id','data'])
        new_ids = Canalyse.unique_ids(self,attack)
        for i in range(len(new_ids)):
            x = attack.loc[attack.id==new_ids[i]]
            y = source.loc[source.id==new_ids[i]]
            x = x.reset_index()
            y = y.reset_index()
            t = y['data'].to_list()
            for j in range(x.shape[0]):
                if x.loc[j,'data'] not in t:
                    res = [x.loc[j,'timestamp'],x.loc[j,'channel'],x.loc[j,'id'],x.loc[j,'data']]
                    data.at[data.shape[0]] = res
        return data
    def match(self,attack1,attack2):
    	data = pd.DataFrame(columns=['timestamp','channel','id','data'])
    	new_ids = Canalyse.unique_ids(self,attack1)
    	for i in range(len(new_ids)):
    		x = attack1.loc[attack1.id==new_ids[i]]
    		y = attack2.loc[attack2.id==new_ids[i]]
    		x = x.reset_index()
    		y = y.reset_index()
    		t = y['data'].to_list()
    		for j in range(x.shape[0]):
    			if x.loc[j,'data'] in t:
    				res = [x.loc[j,'timestamp'],x.loc[j,'channel'],x.loc[j,'id'],x.loc[j,'data']]
    				data.at[data.shape[0]] = res
    	return data
    
    def unique_ids(self,df):
        res = df['id'].to_list()
        ids = [i for n, i in enumerate(res) if i not in res[:n]]
        return ids
    def show_log(self,filename,id):
        with open( filename , 'r+' )  as  file:
            log = file.readlines()
            for i in range(len(log)):
                print("playing id : ",id)
                print(log[i])
                time.sleep(0.12)
                os.system('clear')
    def copy(self,filename1,filename2):
    	f = open(filename1,'r+')
    	f2 = open(filename2,'w+')
    	s = f.read()
    	f2.write(s)
    	f.close()
    	f2.close()



