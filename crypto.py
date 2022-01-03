from flask import Flask, render_template, jsonify, request, Response, url_for, redirect
import requests
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import io
import base64
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from jinja2 import Template


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'button1' in request.form:
        plot_url=0
        xaxis=0
        hist=0
        ses=0
        hwd=0
        yhat=[0]
        yhat2=[0]
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

        if asset=='BTC':
            api_url2 = "https://api.coindesk.com/v1/bpi/historical/close.json"
            response2 = requests.get(api_url2)
            hist = list(response2.json()['bpi'].values())
            hist = [round(float(n),6) for n in hist]
            xaxis = list(response2.json()['bpi'].keys())
            xaxis = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in xaxis]
            
            # single exponential smoothing
            
            # prepare data
            data = hist
            # create class
            model = SimpleExpSmoothing(data)
            # fit model
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(start=31)
            
            # double or triple exponential smoothing
            
            # prepare data
            data = hist
            # create class
            model = ExponentialSmoothing(data,"add", damped=True)
            # fit model
            model_fit = model.fit()
            # make prediction
            yhat2 = model_fit.predict(start=31)
            

            img = io.BytesIO()
            plt.plot(xaxis, hist, marker="o")

            dtFmt = mdates.DateFormatter('%m-%d')
            plt.gca().xaxis.set_major_formatter(dtFmt)

            plt.xlabel("Date")
            plt.ylabel("Closing Price ($)")
            plt.savefig(img,format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
        if len(i) > 0:
            price = response.json()['markets'][i[0]]['price']
            change_24h = response.json()['markets'][i[0]]['change_24h']
            spread = response.json()['markets'][i[0]]['spread']
            volume_24h = response.json()['markets'][i[0]]['volume_24h']
            return render_template('index.html', ses=round(float(yhat[0]),6), hwd = round(float(yhat2[0]),6), plot_url=plot_url, hist=hist, xaxis=xaxis, asset = asset, price=round(float(price),6), change = round(float(change_24h),6), spread = round(float(spread),6), volume = round(float(volume_24h),6))
    return render_template('index.html')




@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
