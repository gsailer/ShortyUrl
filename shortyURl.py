# controller
import logic
import validators
import sqlite3
from flask import Flask, request, render_template, redirect

DATABASE = "urls.db"
TABLE = "urls"
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/", methods=['POST'])
def home_addEntry():
	longUrl = request.form['longURl']
	if not validators.url(longUrl):
		return "Bad input"
	short = logic.addEntry(longUrl, logic.connect(DATABASE), TABLE)
	return "Sucessfully shortened: "+ short

@app.route("/s/<short>")
def router(short):
	longUrl = logic.resolve(short,logic.connect(DATABASE))
	if longUrl == 0:
		return "The shortened Page you are looking for is not available"
	return redirect(longUrl)

if __name__ == "__main__":
    app.run(host='172.24.41.230')