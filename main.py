from flask import Flask , render_template , url_for , request, flash, redirect
import pandas as pd
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "1234"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/about")
def about_me_page():
    return render_template("about_me.html")

@app.route("/automl" , methods = ["GET" , "POST"])
def automl():
    #For now I have not written the logic for the empty file error, gotta figure that out
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        else:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'] , filename)
                file.save(path)
                clean_path = "./static/uploads/{}".format(filename)
                df = pd.read_csv(clean_path)
                display_df = df.head(10)
                #heads = [cols for cols in display_df]
            return render_template('automl.html', tables = display_df.to_html(classes = 'display') , titles = [cols for cols in display_df])
    return render_template("automl.html")

@app.route("/diy" , methods = ["GET" , "POST"])
def diy():
    return render_template("diy.html")

if __name__ == "__main__":
    app.run(debug = True)
    
    