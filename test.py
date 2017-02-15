# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and. We will used subprocess to run command for blast, metrix and analysis

from flask import Flask, request, url_for, render_template, redirect, flash, send_from_directory, jsonify, abort
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import subprocess
from os import rename, listdir
import threading
import sys
import csv
import glob
import urllib2
import subprocess
import pandas as pd
import glob, os, shutil
import numpy
import math


# initialise the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Upload/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['fa', 'fasta'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Rename files in the upload folder
def rename_file():
 path = '/home/abdou/myproject/app/Upload'
 files = os.listdir(path)
 filenames=(list(files))

 G=1
 S=1
 for file in files:
    os.rename(os.path.join(path, file), os.path.join(path, "G"+str(G) + "S" + str(S)+'.fasta'))
    S=S+1
    if S == 4:
     G=G+1
     S=1




@app.route('/')
def index():
    return render_template("about.html")


 
# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation


@app.route('/blast')
def upload_file():
 return render_template("upload.html")


# Route that will process the file upload
@app.route('/<upload>', methods=['POST'])
def upload(upload):
     # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            
    # Rename files in the Upload folder 
    rename_file()
    # Render blast template when files are succesfully uploaded   
    return render_template('blast.html', filenames=filenames) 

# This route runs blast on all files in the upload folder, create a metrix from the csv files 
#and then run analysis. 
@app.route('/results')
def blast_file():
 #command to run the blast
 command= "python localblast.py" 
 subprocess.call(command, shell=True)
 #command to run the matrixproduction
 command= "python MatrixProduction.py"
 subprocess.call(command, shell=True)
 #command to run the analysis
 command= "Rscript SethAnalysis.R"
 subprocess.call(command, shell=True)
 #Render plots and tables generate from the anlysis
 return render_template("results.html")






 

   


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



if __name__ == '__main__':
    app.run(debug=True) 
