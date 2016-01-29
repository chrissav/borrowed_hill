import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__) # create basic Flask app

client = MongoClient(os.environ['ALPINE_DB_1_PORT_27017_TCP_ADDR'], 27017) # creates a mongo db client that connects to the db by IP address and port number.  'ALPINE_DB_1_PORT_27017_TCP_ADDR' is an environment variable of the container IP.

db = client.alpinedb #create the db

@app.route('/') #Route the url to the root direcory

def alpine():

  _items = db.alpinedb.find()
  items = [item for item in _items] # loop through all items in the db

  return render_template('alpine.html', items=items) # render the template with items from the db

@app.route('/new', methods=['POST']) # Post function to add new items to the database via an html form
def new():
  item_doc = {
      'name': request.form['name'],
      'description': request.form['description']
  }

  db.alpinedb.insert_one(item_doc) #insert into db

  return redirect(url_for('alpine')) # redirect back to root dir to refresh the page with new values

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True) # open app to all Ip addresses
