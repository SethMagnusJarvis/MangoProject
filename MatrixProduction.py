import pandas as pd
import glob, os, shutil
import numpy
import math

def fixsort(data):
	#drops NA values
	data = data.dropna(axis=0, how='any')
	#sorts columns by Accession then by FPKM 
	data = data.sort_values(by=['Accession', 'FPKM'])
	#removes instance of Accession which appears becasue of the way files are imported
	data = data[data.Accession != 'Accession']
	
	#checks every record to see if the first value is a number and removes those which are
	for x in data.Accession:
		listy = list(x)
		if listy[0] == '1' or listy[0] == '2' or listy[0] == '3'or listy[0] == '4'or listy[0] == '5'or listy[0] == '6'or listy[0] == '7'or listy[0] == '8'or listy[0] == '9' :
			data = data[data.Accession != x]
			
	#drops duplicate ascession numbers keeping one with highest FPKM (because it's sorted to be at the top)
	data = data.drop_duplicates(subset='Accession')
	return(data)

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
for index, file in enumerate(files):
	if index==0:
		#initialise matrix by loading first file into dataframe
		#read the csv skipping lines which don't have 2 cols (as dictated by making the names mycols)
		mtrix = fixsort(pd.read_csv(path+file, error_bad_lines=False, names=mycols))		
	else:
		#extend datamatrix by merging with subsequent dataframe
		#read the csv
		data = fixsort(pd.read_csv(path+file, error_bad_lines=False, names=mycols))
		# merge data from this file to matrix
		mtrix = pd.merge(mtrix,data, on='Accession', how='outer')
		
#fill empty slots with 0.01
mtrix = mtrix.fillna(0.01)
#replace 0s with 0.01
mtrix = mtrix.replace('0.0', 0.01)
#Change row names
mtrix = mtrix.set_index('Accession', drop=True)
#Tried to change col names below, columns have gone weird though so I'm doing it in R instead for now
#mtrix.columns = ['Accession', 'G1S1', 'G1S2', 'G1S3','GS1', 'G2S2', 'G2S3','G3S1', 'G3S2', 'G3S3']
#output resulting matrix
mtrix.to_csv("CSV/DataSet.csv")
