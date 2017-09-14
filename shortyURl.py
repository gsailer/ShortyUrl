import logic
import validators
from flask import Flask, request, render_template, redirect

DATABASE = "urls.db"
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=['POST'])
def home_addEntry():
    longUrl = request.form['longURl']
    if not validators.url(longUrl):
        return render_template("bad_input.html")
    short = logic.addEntry(longUrl, logic.connect(DATABASE))
    current_url = "/s/" + short
    return render_template("shortened.html", url = current_url, short = short)

@app.route("/s/<short>")
def router(short):
    longUrl = logic.resolve(short, logic.connect(DATABASE))
    if not longUrl:
        return render_template("not_available.html")
	#return "The shortened Page you are looking for is not available"
    return redirect(longUrl)

if __name__ == "__main__":
    app.run()
