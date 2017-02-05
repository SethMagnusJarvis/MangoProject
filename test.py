from flask import Flask, request, url_for, render_template, redirect, flash, send_from_directory
import os
from werkzeug.utils import secure_filename


upload_folder = '/home/abdou/myproject/uploads'
allowed_extensions = set(['fa', 'fasta'])

# initialise the Flask application
app = Flask(__name__)

app.config['UPLOAD_FOLDER']= upload_folder
app.config['ALLOWED_EXTENSIONS'] =allowed_extensions
app.secret_key= "85QSjmqj"


def allowed_file(filename):
 return '.' in filename and \
   filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template("about.html")


@app.route('/blast')
def upload_file():
 return render_template("upload.html")


@app.route('/blast', methods= ['POST'])
def upload():
 # get th name of the uploaded file
 file= request.files['file']
 #check if the file is one of the extensions types allowed
 if file and allowed_file(file.filename):
 #make the file safe, remove unsupported chars
  filename=secure_filename(file.filename)
 
 #move the file from the temporal folder to the upload folder we setup

  file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename)
)
 # redirect the user to the uploaded_file route which will basically show on the browser the uploaded file

  return redirect(url_for("uploaded_file", 
                           filename=filename))



@app.route('/uploads <filename>')
def uploaded_file(filename):
 return send_from_directory(upload_folder, filename)


  



 



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
