from flask import Flask, request, url_for, render_template, redirect
import os
from werkzeug.utils import secure_filename

upload_folder = '/home/abdou/myproject/app/fastafiles'
allowed_extensions = set(['fa', 'fasta'])

app = Flask(__name__)

app.config['upload_folder']= upload_folder


def allowed_file(filename):
 return '.' in filename and \
   filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template("about.html")



@app.route('/blast')
def upload_filepost():
 return render_template("upload.html")



@app.route('/blast', methods = ['GET', 'POST'])
def upload_file():
 
 if request.method == 'POST': # check if the post request has the file path
  if 'file' not in request.files:
    flash('no file path')
    return redirect(request.url) # if user does not select file, browser also submit a an empty part without filename
 file=request.files['file']

 if file.filename == '':
  flash('no selected file')
  return redirect (request.url)

 if file and allowed_file(file.filename):
  filename= secure_filename(file.filename)
  file.save(os.path.join(app.config['upload_folder'], filename))
  return redirect(url_for('uploaded_file', filename=filename))



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
