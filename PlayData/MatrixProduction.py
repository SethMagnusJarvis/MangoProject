import pandas as pd
import glob, os, shutil
import numpy
import math

#move files from upload to CSV for easier future use
source_dir = 'Upload/'
path = 'CSV/'
files = glob.iglob(os.path.join(source_dir, "*.csv"))

for file in files:
    if os.path.isfile(file):
        shutil.copy2(file, path)

#set the locatoin to look for files
files = os.listdir(path)
#produce a list of file names
filenames=(list(files))
AccessionList = []
mycols = ['Accession', 'FPKM']
#Extract ascession codes from every file in directory 
for file in files:
	#read the csv skipping lines which for some reason have 3 commas meaning they're interpreded as 4 sections and locking the length to 2 columns by matching it to the length of my cols 
	data = pd.read_csv(path+file, error_bad_lines=False, names=mycols)
	#remove Nans 
	data = data.dropna(axis=0, how='any')
	#add ascession codes from the file to a list
	AccessionList.extend(data['Accession'])
#print(AccessionList)
#create sorted list of unique ascession codes
AccessionList = list(set(AccessionList))
AccessionList.sort()

#remove all numbers and the instance of Accession which appears becasue of the way files are imported
x=0
while x<length:
	name = AccessionList[x]
	item = list(name)
	if item[0] == "1" or item[0] == "2" or item[0] == "3" or item[0] == "4" or item[0] == "5" or item[0] == "6" or item[0] == "7" or item[0] == "8" or item[0] == "9":
		AccessionList.remove(name)
		continue
	if name == 'Accession':
		AccessionList.remove(name)
		#breaks the loop becasue ascession is the last incorrect value (It's possible that this could be made more effecient by using a for loop but when I started I was using indexing)
		break
	x=x+1
