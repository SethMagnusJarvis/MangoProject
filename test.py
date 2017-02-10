# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded

from flask import Flask, request, url_for, render_template, redirect, flash, send_from_directory, jsonify, abort
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import subprocess
from os import rename, listdir
import threading
import uuid
import sys
import csv
import glob
import urllib2
import subprocess


# initialise the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['fa', 'fasta'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# rename files in the uploads folder
def rename_file():
 path = '/home/abdou/myproject/app/uploads'
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

# run blast in the background 
#background_scripts={}

#def run_script(id):
 #subprocess.call(["/home/abdou/myproject/app/blast.py", "sequence", "gbk"])
 #background_script[id]=True


#blast function 
def blast_sequence(sequence):
    # Write sequence into file to blast
    with open("sequence.fasta", "w") as fasta_sequence:
        fasta_sequence.write(">%s" % sequence)

    # Blast sequence
    command = "blastn -db Database/BtVrDb -outfmt '6 qseqid sseqid pident' -query sequence.fasta -out sequence.out "
    subprocess.call(command, shell=True)

    # Get GI, accession number and FPKM value
    lines = open("sequence.out").readlines()
    if lines:
        lines = lines[0].replace("\t", "|").split("|")
        gene_gi = lines[2]
        accession_number = lines[4]
        label, fpkm_value = sequence.split("\n")[0].split()[:]

        # Remove temporary files
        subprocess.call("rm -f sequence.fasta sequence.out", shell=True)

        return [accession_number, fpkm_value]

    return ["", "", "", ""]


# Start program
if __name__ == '__main__':

    # Check if one need to use blast databases remotelly or not
    remote_arg = ""
    if len(sys.argv) > 1 and sys.argv[1] == "-remote":
        remote_arg = "-remote"

    # Input species, delimeter is comma or space
    #species = []
    #while not species:
    #    species = raw_input("Enter species: ")
    #    species = species.replace(",", " ").split()

    # Read FASTA files and fix header line format
    for fasta in glob.glob(os.path.join("uploads", "*.fasta")):
        # Skip fixed file
        if "_fixed.fasta" in fasta:
            continue

        print "Fixing file %s ..." % fasta
        basename, ext = os.path.splitext(fasta)
        with open(basename + "_fixed" + ext, "wb") as fasta_fixed:
            # Read content of original FASTA file
            for line in open(fasta):
                # Replace "_" by "-"
                line = line.replace("_", "-")

                # Replace ";" by " "
                line = line.replace(";", " ")

                # Insert '>'
                if "-" in line:
                    line = ">%s" % line

                # Write fixed text to new file ends with "_fixed"
                fasta_fixed.write(line)

    # BLAST fasta files and find gene
    for fasta in glob.glob(os.path.join("uploads", "*_fixed.fasta")):
        print "Blast file %s ..." % fasta

        # Open CSV file to write results
        report = fasta.replace("_fixed.fasta", ".csv")
        with open(report, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Accession Number", "FPKM Value"])

            # Iterate via sequences
            sequence = ""

            for line in open(fasta):
                if line.startswith('>') and sequence.startswith('>'):
                        # Run blast
                        row = blast_sequence(sequence)
                        # Save row
                        writer.writerow(row)
                        # Start new sequence
                        sequence = line
                else:
                    sequence += "%s\n" % line

            # If the last sequence is not empty
            if sequence and sequence.startswith('>'):
                # Run blast
                row = blast_sequence(sequence)
                # Save row
                writer.writerow(row)




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
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file

    rename_file()     
    return render_template('home.html', filenames=filenames) # files uploaded succesfully, click here to run blast

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and run blast
@app.route('/uploads/<filename>')
def uploaded_file(filename):
 for filenames in app.config['UPLOAD_FOLDER'], filename:
  blast_sequence(filenames)
 #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#This route will run the blast in the background and save the results in the saver

#@app.route('/generate')
#def generate():
 #   id = str(uuid.uuid4())
  #  background_scripts[id] = False
   # threading.Thread(target=run_script(id)).start()
    #return render_template('processing.html', id=id)


#This route will show if processed is done
#@app.route("/is_done")
#def is_done():
 #id= request.args.get("id", None)
 #if id not in background_scripts:
  #abort(404)
 #return jsonify(done=background_scripts[id])
 

   
    




     








#@app.route('/result)
#def blast():
 #memory = subprocess.Popen(['blast.py, UPLO'],stdout=subprocess.PIPE])
 #out,error = memory.communicate()

# return render_template('view.html', out=out, error=error)





  



 



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
