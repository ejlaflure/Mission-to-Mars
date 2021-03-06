# Import Dependancies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Flask route for the index HTML page.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Flask Srapping Route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.replace_one({}, mars_data, True)
   return redirect("/")

# Running Flask App
if __name__ == "__main__":
   app.run()