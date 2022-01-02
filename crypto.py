from flask import Flask, render_template, jsonify, request, Response, url_for, redirect
import requests
from jinja2 import Template


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'button1' in request.form:
        api_url = "https://www.cryptingup.com/api/markets"
        response = requests.get(api_url)
        asset=request.form['asset']
        h = 0
        i = []
        for x in response.json()['markets']:
            if x['base_asset'] == asset:
                i.append(h)
                break
            else:
                h += 1

        if len(i) > 0:
            price = response.json()['markets'][i[0]]['price']
            change_24h = response.json()['markets'][i[0]]['change_24h']
            spread = response.json()['markets'][i[0]]['spread']
            volume_24h = response.json()['markets'][i[0]]['volume_24h']

    return render_template('index.html', price=price, change = change_24h, spread = spread, volume = volume_24h)




@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)