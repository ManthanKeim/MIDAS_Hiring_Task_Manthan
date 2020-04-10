import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from nltk.corpus import stopwords
import sklearn
import pickle
import praw
import re
from bs4 import BeautifulSoup
import nltk
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = '/Users/manthan/Documents/Projects/MIDAS_final/uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = pickle.load(open('model.pkl', 'rb'))

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def detect(link):
    link2 = str(link)
    reddit = praw.Reddit(client_id='D4LOJoob-A5kag', client_secret='hevxVvuNzRImaqeWx1l8f3-fATw', user_agent='MIDAS')
            
    int_features = link
    processed_text = int_features.lower()
    print(processed_text)
    

    submission = reddit.submission(url=processed_text)
        
    data = {}

    data['title'] = submission.title
    data['title_un'] = submission.title
    data['url'] = submission.url
    data['selftext'] = submission.selftext

    submission.comments.replace_more(limit=None)
    comment = ''
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
    data["comment"] = comment
    data['title'] = clean_text(data['title'])
    data['comment'] = clean_text(data['comment'])
    data['combine'] = data['title'] + data['comment'] + data['url']
        
        
    #    prediction = model.predict(int_features)

    output = model.predict([data['combine']])
    
    return format(output)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text):
    
    text = BeautifulSoup(text, "lxml").text
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    reddit = praw.Reddit(client_id='D4LOJoob-A5kag', client_secret='hevxVvuNzRImaqeWx1l8f3-fATw', user_agent='MIDAS')
    
    int_features = request.form['redditurl']
    processed_text = int_features.lower()
    print(processed_text)
    

    submission = reddit.submission(url=processed_text)
        
    data = {}

    data['title'] = submission.title
    data['title_un'] = submission.title
    data['url'] = submission.url
    data['selftext'] = submission.selftext

    submission.comments.replace_more(limit=None)
    comment = ''
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
    data["comment"] = comment
    data['title'] = clean_text(data['title'])
    data['comment'] = clean_text(data['comment'])
    data['combine'] = data['title'] + data['comment'] + data['url']
    
    
#    prediction = model.predict(int_features)

    output = model.predict([data['combine']])
    print(output)
    
    return render_template('index.html', prediction_text='The flair for the subreddit post is : {}'.format(output))
    

@app.route('/about',methods=['POST'])
def about():
    
    reddit = praw.Reddit(client_id='D4LOJoob-A5kag', client_secret='hevxVvuNzRImaqeWx1l8f3-fATw', user_agent='MIDAS')
    
    int_features = request.form['redditurl']
    processed_text = int_features.lower()
    print(processed_text)
    
    data = {}
    submission = reddit.submission(url=processed_text)
    
    data['title'] = submission.title
    data['title_un'] = submission.title
    data['url'] = submission.url
    data['selftext'] = submission.selftext
    
    return render_template('about.html', title = data['title_un'], About = data['selftext'])

@app.route('/automated_testing',methods=['POST'])
def atest():

        
    lis1 = []
    lis2 = []
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
    
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        with open(filename) as f:
            content = f.readlines()
        for x in content:
            lis1.append(x)
        for i in lis1:
            lis2.append(detect(i))
        fin = {}
        for key in lis1:
            for value in lis2:
                fin[key] = value
                lis2.remove(value)
                break
        return jsonify(fin)
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
    

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
