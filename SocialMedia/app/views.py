"""
Twitter content/media display in personal website br using Twitter API.
"""

# Imports
from app import app
from app import scrap

from flask import render_template, json, jsonify, Response, request, redirect


# Default Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Default route for get_Twitter_Data() method
@app.route('/api/getTwitter')
def get_tweets():
    scrap.get_Twitter_Data()
    return redirect('/') 

# Default route for get_Tumblr_Data() method
@app.route('/api/getTumblr')
def get_tumblr():
    scrap.get_Tumblr_Data()
    return redirect('/') 

# endpoint for the API tp get tweet data from MongoDB and disaply on website
@app.route('/api/viewTweets')
def view_tweets():
    # empty array to store data
    output = []
    #get data from MongoDB and store it in the array
    for s in scrap.twitterCol.find():
        del s['_id']
        output.append(s)
    #create json object to pass to template
    data = { "data": output }
    return jsonify(data)

# endpoint for the API to get Tumblr posts from MongoDB and display on the site
@app.route('/api/viewTumblr')
def view_tumblr():
    # empty array to store data
    output = []
    #get data from MongoDB and store it in the array
    for s in scrap.tumblrCol.find():
        del s['_id']
        output.append(s)
    #create json object to pass to template
    data = { "data": output }
    return jsonify(data)

    