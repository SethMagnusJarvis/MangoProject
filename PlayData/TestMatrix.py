import pandas as pd
import os

path = '/home/vagrant/PlayData/CSV/'
files = os.listdir(path)
filenames=(list(files))
AccessionList = []
data = pd.read_csv("CSV/G1S1.csv")
print(data['Accession'])
#for file in files:
#	data = pd.read_csv(path+file)
#	AccessionList.extend(data['Accession'])

