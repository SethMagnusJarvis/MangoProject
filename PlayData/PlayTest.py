import pandas as pd
import glob, os, shutil
import numpy
import math

path = 'CSV/'
files = os.listdir(path)
filenames=(list(files))
AccessionList = []
mycols = ['Accession', 'FPKM']
data = pd.read_csv('CSV/G1S1.csv', error_bad_lines=False, names=mycols)

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

def fixsort(data):
	#drops NA values
	data = data.dropna(axis=0, how='any')
	#sorts columns by Accession then by FPKM
	data = data.sort_values(by=['Accession', 'FPKM'])
	#removes instance of Accession which appears becasue of the way files are imported
	data = data[data.Accession != 'Accession']
	for x in data.Accession:
		listy = list(x)
		if listy[0] == '1' or listy[0] == '2' or listy[0] == '3'or listy[0] == '4'or listy[0] == '5'or listy[0] == '6'or listy[0] == '7'or listy[0] == '8'or listy[0] == '9' :
			data = data[data.Accession != x]
	#drops duplicate ascession numbers keeping one with highest FPKM
	data = data.drop_duplicates(subset='Accession')
	print(data)	


data=fixsort(data)




	
	
