from flask import Flask, render_template, flash, request
import requests
import urllib.request
import json

# create a flask instance 
app = Flask(__name__)
# Add databasde
#Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
# secret key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"


@app.route('/')

def index():
    first_name = "Archie"
    return render_template("index.html", first_name=first_name,)


username = "chief_berserker"
password = "6aea36b0"
 
# Base URL for Imgflip API
base_url = "https://api.imgflip.com"
 
# Function to get available meme templates
def get_meme_templates():
    response = requests.get(f"{base_url}/get_memes")
    templates = response.json()["data"]["memes"]
    return templates
 
# Function to generate a meme using template ID and text
def generate_meme(template_id, text0, text1):
    params = {
        "template_id": template_id,
        "username": username,
        "password": password,
        "text0": text0,
        "text1": text1,
    }
    response = requests.post(f"{base_url}/caption_image", params=params)
    meme_url = response.json()["data"]["url"]
    return meme_url
 
@app.route('/meme_generator', methods=['GET', 'POST'])
def meme_generator():
    if request.method == 'POST':
        template_id = request.form['template']
        text0 = request.form['text0']
        text1 = request.form['text1']
        meme_url = generate_meme(template_id, text0, text1)
        return render_template('meme_form.html', templates=get_meme_templates(), meme_url=meme_url)
 
    return render_template('meme_form.html', templates=get_meme_templates(), meme_url=None)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)