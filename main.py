from flask import Flask, request, render_template, url_for
import pandas as pd
import json
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from utils import get_clusters
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
    return {'metros': result}

@app.route('/get_ground_stops', methods=['GET'])
def get_ground_stops(request):
    n_clusters = 200
    agg = {'n_lines': 'size'}
    lat_min = float(request.args.get('lat_min'))
    lon_min = float(request.args.get('lon_min'))
    lat_max = float(request.args.get('lat_max'))
    lon_max = float(request.args.get('lon_max'))
    df = pd.read_csv('/home/tserekh/groud_stops.csv')

    filt = (df['lat'] > lat_min) & (df['lat'] < lat_max) & (df['lon'] > lon_min) & (df['lon'] < lon_max)
    df = df[filt]
    if len(df):
        df_clusters = get_clusters(df, n_clusters, agg, 'stupid')
        df_clusters.rename(columns={'n_lines': 'n_ground_stops'}, inplace=True)
        context = {
            'ground_stops': list(df_clusters.T.to_dict().values()),
        }
    else:
        context = {
            'ground_stops': [],
        }

    return context

@app.route('/get_orgs', methods=['GET'])
def get_orgs():
    return {}

@app.route('/get_homes', methods=['GET'])
def get_homes():
    lat_min = float(request.args.get('lat_min'))
    lon_min = float(request.args.get('lon_min'))
    lat_max = float(request.args.get('lat_max'))
    lon_max = float(request.args.get('lon_max'))
    df = pd.read_csv('homes1.csv', sep='\t')
    filt = (df['lat'] > lat_min) & (df['lat'] < lat_max) & (df['lon'] > lon_min) & (df['lon'] < lon_max)
    df = df[filt]
    colored_homes = request.GET.get('colored_homes') == 'true'
    print(colored_homes, 'colored_homes')
    # use_nat_classes = request.GET.get('nat_classes').split('_')
    # max_colored_count = 3000
    n_clusters = 100
    agg = {'flat_num': 'sum'}

    print(df.head())
    df_clusters = get_clusters(df, n_clusters, agg, 'stupid')
    context = {
        'homes': list(df_clusters.T.to_dict().values()),
    }
    return context

if __name__ == "__main__":
    app.run(port=5000, debug=True)
