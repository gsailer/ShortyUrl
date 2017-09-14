import yaml
import logic
import validators
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

@app.route(cfg['web_paths']['main'])
def home():
    return render_template("home.html", title=cfg['general']['title'], url=cfg['web_paths']['main'])


@app.route(cfg['web_paths']['main'], methods=['POST'])
def home_addEntry():
    longUrl = request.form['longURl']
    if not validators.url(longUrl):
        return render_template("bad_input.html", title=cfg['general']['title'])
    short = logic.addEntry(longUrl, logic.connect(cfg['general']['sqlite_location']))
    current_url = cfg['web_paths']['shortened'] + short
    return render_template("shortened.html", url=current_url, short=short, title=cfg['general']['title'])


@app.route(cfg['web_paths']['shortened']+"<short>")
def router(short):
    longUrl = logic.resolve(short, logic.connect(cfg['general']['sqlite_location']))
    if not longUrl:
        return render_template("not_available.html", title=cfg['general']['title'])
    return redirect(longUrl)


if __name__ == "__main__":
    app.run()