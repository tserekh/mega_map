from flask import Flask, request, render_template, url_for
import pandas as pd
import json
from django.http import HttpResponse, JsonResponse
from django.conf import settings

settings.configure(DEBUG=True)
app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
@app.route('/', methods=['POST', 'GET'])
def show_map():
    return render_template('points.html', have_logos=[])


@app.route('/get_metros', methods=['GET'])
def get_metros():

    lat_min = float(request.args.get('lat_min'))
    lon_min = float(request.args.get('lon_min'))
    lat_max = float(request.args.get('lat_max'))
    lon_max = float(request.args.get('lon_max'))
    df = pd.read_csv('/home/tserekh/metro.csv')

    filt = (df['lat'] > lat_min) & (df['lat'] < lat_max) & (df['lon'] > lon_min) & (df['lon'] < lon_max)
    df = df[filt]
    result = list(df.T.to_dict().values())
    return json.loads(json.dumps({'metros': result}))

@app.route('/get_orgs', methods=['GET'])
def get_orgs():

    lat_min = float(request.args.get('lat_min'))
    lon_min = float(request.args.get('lon_min'))
    lat_max = float(request.args.get('lat_max'))
    lon_max = float(request.args.get('lon_max'))
    df = pd.read_csv('/home/tserekh/metro.csv')

    filt = (df['lat'] > lat_min) & (df['lat'] < lat_max) & (df['lon'] > lon_min) & (df['lon'] < lon_max)
    df = df[filt]
    result = JsonResponse(list(df.T.to_dict().values()), safe = False)
    return json.dumps({'orgs': result})
if __name__ == "__main__":
    app.run(port=5000, debug=True)
