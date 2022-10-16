from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

## Use flask_pymongo to set up mongo connection
# Tells Python that our app will connect to Mongo 
# using a URI, a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
# Index.html is the default HTML file we'll use to display the content we've scraped
@app.route("/")  # tells Flask what to display when we're looking at the home page
def index():
   mars = mongo.db.mars.find_one()  # uses PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars)  
# tells Flask to return an HTML template using an index.html file
# tells Python to use the "mars" collection in MongoDB.


# Set up the scraping route 
# This will be tied to a button on the home page
# Defines route that Flask will use. This route will run the below function.
@app.route("/scrape")
# Define function
def scrape():
   # Assign variable that points to Mongo database
   mars = mongo.db.mars
   # Assign variable to hold the data scraped in the scraping.py file
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # Navigate our page back to / where we can see the updated content
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()