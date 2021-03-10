from flask import Flask, request, render_template, url_for
from manage MetroStation
import pandas as pd
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def show_map():
    return render_template('points.html', have_logos=[])


@app.route('/get_metros', methods=['GET'])
def get_metros(request):

    lat_min = request.GET.get('lat_min')
    lon_min = request.GET.get('lon_min')
    lat_max = request.GET.get('lat_max')
    lon_max = request.GET.get('lon_max')
    df = pd.read_csv('/home/tserekh/metro.csv')

    filt = (df['lat'] > lat_min) & (df['lat'] < lat_max) & (df['lon'] > lon_min) & (df['lon'] < lon_max)
    df = df[filt]
    return {'metros':list(df.T.to_dict().values())}
if __name__ == "__main__":
    app.run(port=5000, debug=True)
