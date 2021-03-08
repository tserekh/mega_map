import sys
sys.path.append('/usr/lib/python3/dist-packages')


from collections import defaultdict
import json
import glob
from tqdm import tqdm
import requests
import math
import pandas as pd
import numpy as np
import itertools
from sklearn.cluster import KMeans

import time
import random
from pyproj import Proj, transform

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Min, Sum
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.conf import settings
from django import template  
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Min, Sum

from .models import Organization,OrganizationNatClass, House, MetroStation, Metro
from .models import PolygonModel, LineModel, GroundStop, OperSquare, SalePoint
from .models import PredictedSquare, Distance, TimeSquare
from PIL import Image

SERVER_URL = 'http://178.62.250.186'
#SERVER_URL = 'http://127.0.0.1'
SERVER_URL_MSK_DRIVING = SERVER_URL + ':5000/table/v1/driving/'
SERVER_URL_MSK_FOOT = SERVER_URL + ':5001/table/v1/foot/'
SERVER_URL_PETER_DRIVING = SERVER_URL + ':5002/table/v1/driving/'
SERVER_URL_PETER_FOOT = SERVER_URL + ':5003/table/v1/foot/'

PROJ3857  = Proj("+init=EPSG:3857")
PROJ4326 = Proj("+init=EPSG:4326")

def income_index_to_income(x):
    if x<=1:
        return x*12000
    elif x<=2:
        return 12000 + (x-1)*(46000 - 12000)
    elif x<=3:
        return 46000 + (x-2)*(46000 - 100000)
    else:
        return 100000 + (x-3)*(100000 - 150000)

def get_min_distance(nearest_nat_classes_euclid, use_nat_classes):
    dic = json.loads(nearest_nat_classes_euclid)
    distances_set = set()
    for use_nat_class in use_nat_classes:
         if use_nat_class in dic.keys():
            distances_set |= set(dic[use_nat_class])
    if len(distances_set)==0:
        distance_min = -1
    else:
        distance_min = min(distances_set)
    return distance_min

def get_have_logos():
    have_logos = glob.glob('main_map/static/map_icons/*')
    dic = {}
    for have_logo in have_logos:
        
        im = Image.open(have_logo)
        width, height = im.size
        square = width*height
        
        have_logo = have_logo.split('/')[-1]
        have_logo = '.'.join(have_logo.split('.')[:-1])
        dic[have_logo] = width
    return dic

@login_required
def conver_to_list(pol):
    '''
    Convert POLYGON(()) in string format to list of lists of coords
    '''
    pol = pol.replace('POLYGON ((','')
    pol = pol.replace(')','')
    #change lat-lon to lon-lat
    pol = list(map(lambda x: [float(x.split(' ')[1]),float(x.split(' ')[0])]  , pol.split(', ')))
    return pol

@login_required
def index(request):
    have_logos = get_have_logos()
    #have_logos = glob.glob('static/map_icons/*')

    filter_dic = {
                    'lat__gt' : 55.668926,
                    'lon__gt' : 37.462978,
                    'lat__lt' : 55.702117,
                    'lon__lt' : 37.574429
    }

    context = {
        #'metros': mark_safe(serializers.serialize("json", Metro.objects.all())),
        'metros': {},
        #'orgs': mark_safe(serializers.serialize("json", Organization.objects.filter(**filter_dic,eng_class='supermarket'))),
        'orgs': mark_safe({}),
        'homes': mark_safe(serializers.serialize("json", House.objects.filter(**filter_dic))),
        'have_logos': mark_safe(have_logos),
        #'questions': questions,
    }
    
    return render(request, 'main_map/points.html',context)

def get_oper_squares(request):
    t0 = time.time()
    print(time.time() - t0)
    filter_dic = {
        'y__gt' : float(request.GET.get('y_min')) - 500,
        'x__gt' : float(request.GET.get('x_min')) - 500,
        'y__lt' : float(request.GET.get('y_max')) + 500,
        'x__lt' : float(request.GET.get('x_max')) + 500,
        
        'income__lte' : request.GET.get('income_max'),
        'income__gte' : request.GET.get('income_min'),
        
        'age__lte' : request.GET.get('age_max'),
        'age__gte' : request.GET.get('age_min'),
    }

    to_mean = request.GET.get('to_mean');
    users_min = float(request.GET.get('users_min'))
    users_max = float(request.GET.get('users_max'))
    if request.GET.get('homes')!=request.GET.get('works'):
        if request.GET.get('homes')=='true':
            filter_dic['if_home'] = True
        else:
            filter_dic['if_home'] = False
            
            
    if request.GET.get('male')!=request.GET.get('female'):
        if request.GET.get('male')=='true':
            filter_dic['male'] = True
        else:
            filter_dic['male'] = False
    print(time.time() - t0)        
    objects = OperSquare.objects.filter(**filter_dic)
    if objects.count()==0:
        context = {
            'oper_squares':[],
            'max_result': 0,
            }
        return JsonResponse(context,safe = False)
    
    df = pd.DataFrame(list(objects.values()))
    
    if to_mean=='null':
        df = pd.DataFrame(list(objects.values(*['x','y']).annotate(Sum('users'))))
        
        filt1 = df['users__sum'] >= users_min
        filt2 = df['users__sum'] <= users_max
        #df = df[filt1&filt2]
        df = df[filt1]
        df = df.rename(columns ={'users__sum':'result','source_id':'size'})
        print(time.time() - t0)
    else:
        df['mult'] = df['users']*df[to_mean]
        agg = {}
        agg['mult'] = sum
        agg['x'] = lambda x: x.iloc[0]
        agg['y'] = lambda x: x.iloc[0]
        df = df.dropna()
        
        df_gb1 = df.groupby('source_id').agg(agg)

        df_gb2 = df.groupby('source_id')[['users']].sum()
        
        filt1 = df_gb2['users'] >= users_min
        filt2 = df_gb2['users'] <= users_max
        #df_gb2 = df_gb2[filt1&filt2]
        df_gb2 = df_gb2[filt1]
        
        df = pd.merge(df_gb1.reset_index(), df_gb2.reset_index(),on='source_id',how='inner')
        print(df.head())
        df['result'] = df['mult']/df['users']
        
    print(time.time() - t0)            
    print('mean_result',df['result'].mean())
    print('mean_result',df['result'].mean())
    pretty_dic = {}
    pretty_dic['null'] = lambda x: 'Число людей ' + str(np.round(2.7*x))
    pretty_dic['age'] =  lambda x: 'Средний возраст ' + str(int((42/3.5)*x)) if x<6 else 'Средний возраст более 64'
    pretty_dic['male'] = lambda x: 'Мужчин ' + str(np.round(100*x,2)) + '%' + '<br/>' +  'Женщин ' +  str(np.round(100*(1-x),2)) + '%'
    pretty_dic['income'] = lambda x: 'Средний доход ' + str(int((56700/1.42)*x)) if x<3 else 'Средний доход более 100000'
    pretty_dic['if_home'] = lambda x: 'Жителей '+str(np.round(100*x/(1+x),2)) + '%'+'<br/>'+'Рабочих ' + str(np.round(100/(1+x),2))+'%'
    df['pretty_result'] = df['result'].apply(pretty_dic[to_mean])
    
    context = {
        'oper_squares': list(df[['x','y','result','pretty_result']].T.to_dict().values()),
        'max_result': df['result'].max(),
        }
    
    return JsonResponse(context,safe = False)

def get_metros(request):
    filter_dic = {
                'lat__gt' : request.GET.get('lat_min'),
                'lon__gt' : request.GET.get('lon_min'),
                'lat__lt' : request.GET.get('lat_max'),
                'lon__lt' : request.GET.get('lon_max'),
    }
    
    count = Metro.objects.filter(**filter_dic).count()
    max_count = 60
    if count < max_count:
        objects = Metro.objects.filter(**filter_dic)
    else:
        objects = MetroStation.objects.filter(**filter_dic)
        
    context = {
        'metros': serializers.serialize("json",objects ),
    }
    
    return JsonResponse(context,safe = False)

def get_ground_stops(request):
    n_clusters = 200
    agg = {'n_lines':'size'}
    filter_dic = {
                'lat__gt' : request.GET.get('lat_min'),
                'lon__gt' : request.GET.get('lon_min'),
                'lat__lt' : request.GET.get('lat_max'),
                'lon__lt' : request.GET.get('lon_max'),
    }
    
    objects = GroundStop.objects.filter(**filter_dic)
    if objects.count():
    
        df = pd.DataFrame(list(objects.values()))
        df_clusters = get_clusters(df, n_clusters, agg, 'stupid')
        df_clusters.rename(columns = {'n_lines':'n_ground_stops'}, inplace=True)
        context = {
            'ground_stops': list(df_clusters.T.to_dict().values()),
        }
    else:
        context = {
            'ground_stops': [],
        }
    
    return JsonResponse(context,safe = False)

def get_homes(request):
    filter_dic = {
                'lat__gt' : request.GET.get('lat_min'),
                'lon__gt' : request.GET.get('lon_min'),
                'lat__lt' : request.GET.get('lat_max'),
                'lon__lt' : request.GET.get('lon_max'),
    }
    

    lat_max = request.GET.get('lat_max')
    lon_max = request.GET.get('lon_max')
    
    lat_min = request.GET.get('lat_min')
    lon_min = request.GET.get('lon_min')    
    
    x_max, y_max = transform(PROJ4326, PROJ3857, lon_max, lat_max)
    x_min, y_min = transform(PROJ4326, PROJ3857, lon_min, lat_min)
    
    colored_homes = request.GET.get('colored_homes')=='true'
    print(colored_homes, 'colored_homes')
    use_nat_classes = request.GET.get('nat_classes').split('_')
    max_colored_count = 3000
    
    features = ['flat_num', 'x', 'y', 'address', 'source_id','source_name','sale_price']
    objects = House.objects.filter(**filter_dic).values().values_list(*features)
    if objects.count() > max_colored_count:
        colored_homes = False
    df = pd.DataFrame(list(objects.values()), columns=features)

    n_clusters = 100
    
    if colored_homes:
        distance_name = 'euclid_distance'
        df, df_orgs = brand_map(lat_min, lon_min, lat_max, lon_max, use_nat_classes, distance_name, filter_dic)
    df = df.rename(columns = {'euclid_distance':'min_distance'})

    agg = {'flat_num':'sum'}
    if colored_homes:
        agg['min_distance'] = 'mean'
        agg['chain_name'] = lambda x: list(x)[0] if len(x)!=0 else '-'
        #agg['min_distance_metro'] = 'mean'
        print('to cluster')
    print(df.head())
    df_clusters = get_clusters(df, n_clusters, agg, 'stupid')
    context = {
        'homes': list(df_clusters.T.to_dict().values()),
        
    }
    
    return JsonResponse(context,safe = False)

    
def get_orgs(request):
    coord_filter_dic = {
                'lat__gt' : request.GET.get('lat_min'),
                'lon__gt' : request.GET.get('lon_min'),
                'lat__lt' : request.GET.get('lat_max'),
                'lon__lt' : request.GET.get('lon_max'),   
    }
    
    lat_max = request.GET.get('lat_max')
    lon_max = request.GET.get('lon_max')
    
    lat_min = request.GET.get('lat_min')
    lon_min = request.GET.get('lon_min')   
    
    if request.GET.get('nat_classes') is not None:
        nat_class_filter_dic = {
            'nat_class__in': request.GET.get('nat_classes').split('_'),
        }
    else:
        nat_class_filter_dic = {}
    
    if request.GET.get('chain_name') is not None:
        chain_name_filter_dic = {
            'chain_name__in': request.GET.get('chain_name').split('_'),
        }
    else:
        chain_name_filter_dic = {}
    count_customers = request.GET.get('point_count')=='true'
    
    features = ['nat_class', 'source_id','chain_name','lat','lon','address','source_name']
    filt = Q(**coord_filter_dic)&(Q(**nat_class_filter_dic)|Q(**chain_name_filter_dic))
    objects = OrganizationNatClass.objects.filter(filt).values().values_list(*features)
    n_clusters = 200
    if objects.count()>n_clusters:
        count_customers = False
    if request.GET.get('heat_map')=='false':
        print('point_count', request.GET.get('point_count'))
        if count_customers:
            print('\npoint_count\n')
            distance_name = 'euclid_distance'
            _, df = brand_map(
                                    lat_min,
                                    lon_min,
                                    lat_max,
                                    lon_max,
                                    request.GET.get('nat_classes').split('_'),
                                    distance_name,
                                    coord_filter_dic)
        else:


            df = pd.DataFrame(list(objects), columns=features)
            df = df.drop_duplicates(['source_id', 'source_name'])
        
        agg = {}
        agg['chain_name'] = lambda x: list(x)[0] if len(x)==1 else '-'
        if count_customers:
            agg['flat_num'] = sum
        print('*******************************')
        print(df.head())
        df_clusters =  get_clusters(df, n_clusters, agg, 'stupid')
        need_cols = ['x','y','count','is_one','chain_name']
        if len(df) < n_clusters:
            need_cols.append('chain_name')
        if count_customers:    
            need_cols.append('flat_num')
        need_cols = sorted(set(need_cols) & set(df_clusters.columns))
        context = {
            'orgs': list(df_clusters[need_cols].T.to_dict().values()),
        }
        return JsonResponse(context, safe = False)
    
    else:
        features = ['x','y']
        filt = Q(**coord_filter_dic)&(Q(**nat_class_filter_dic)|Q(**chain_name_filter_dic))
        objects = OrganizationNatClass.objects.filter(filt).values().values_list(*features)
        need_cols = features.copy()
        df = pd.DataFrame(list(objects), columns=features)
        context = {
            'orgs': list(df[need_cols].T.to_dict().values()),
        }
        return JsonResponse(context, safe = False)
def get_polygons(request):
    
    filter_dic = {
                #'lat__gt' : request.GET.get('lat_min'),
                #'lon__gt' : request.GET.get('lon_min'),
                #'lat__lt' : request.GET.get('lat_max'),
                #'lon__lt' : request.GET.get('lon_max'),
                #'scale' : request.GET.get('scale'),
                'scale' : 'district',
    }
    need_cols = ['points','eng_name','flat_num','sale_price']
    #need_cols = ['eng_name','flat_num','sale_price']
    max_count = 1000
    objects = PolygonModel.objects.filter(**filter_dic).values().values_list(*need_cols)[:max_count]
    df = pd.DataFrame(list(objects), columns = need_cols)
    df['points'] = df['points'].apply(conver_to_list)
    context = {
        'polygons': list(df.T.to_dict().values()),
        #'polygons':{},
    }
    return JsonResponse(context, safe = False)
def get_lines(request):
    filter_dic = {
        'lat0__gt' : request.GET.get('lat_min'),
        'lon0__gt' : request.GET.get('lon_min'),
        'lat0__lt' : request.GET.get('lat_max'),
        'lon0__lt' : request.GET.get('lon_max'),

        #'mode' : request.GET.get('mode'),
        #'att' : request.GET.get('att'),
        'mode':'foot',
        'att':'metro',
        }
    
    need_cols = ['lat0','lon0','lat1','lon1', 'weight']
    objects = LineModel.objects.filter(**filter_dic).values()
    zone_count = objects.count()
    if (zone_count>1E4)|(zone_count==0):
        context = {
            'lines': [],
            'zone_count':zone_count,
        }
    else:
        objects = objects.values_list(*need_cols).order_by('-weight')[:3000]
        df = pd.DataFrame(list(objects), columns = need_cols)
        df = df.sort_values('weight', ascending = True)

        df['line'] = df.apply(lambda x: [[x['lon0'], x['lat0']],[x['lon1'], x['lat1']]],axis = 1)
        response_cols = ['line','weight']
        context = {
            'lines': list(df[response_cols].T.to_dict().values()),
            'zone_count':zone_count,
        }
    return JsonResponse(context, safe = False)
def cacl_sale_point(request):
    x = float(request.GET.get('x'))
    y = float(request.GET.get('y'))
 
    sale_point = SalePoint(x=x, y=y)
    sale_point.cann = ''
    sale_point.revenue_pred_model1 = 1e6*(1 + random.random()/3)
    sale_point.save()
    
    sale_point.cann = json.dumps(get_cann_dict(x,y))
    sale_point.comp = json.dumps(get_comp_dict(x,y))
    
#     features_dic = get_place_features(sale_point.x,sale_point.y)
#     sale_point.machine_features = json.dumps(features_dic)
    
#     dic = json.loads(sale_point.machine_features)
#     sale_point.revenue_pred_model1 = dic['Магазин бытовой техники и электроники_1']
#     sum_ = 0
#     sum_ += dic['Магазин бытовой техники и электроники_1']
#     sum_ += dic['Магазин бытовой техники и электроники_2']
#     sum_ += dic['Магазин бытовой техники и электроники_3']
#     sum_ += dic['Магазин бытовой техники и электроники_4']
#     sum_ += dic['Магазин бытовой техники и электроники_5']
#     sale_point.revenue_pred_model2 = sum_ 
    
    
#     coords, times = get_coord_time(x, y, 50, 5000, mode='driving')
#     sale_point.isocrone_coords = json.dumps(coords)
#     sale_point.isocrone_times = json.dumps(times)
    
#     sale_point.save()
    context = {
        'x':x,
        'y':y,
    }
    return JsonResponse(context, safe = False)

def get_isocrone(request):
    sale_point = SalePoint.objects.find()
    
    coords = json.loads(sale_point.isocrone_coords)
    times = json.loads(sale_point.isocrone_times)
    
    
    context = {
        'coords':coords,
        'times': times,
    }
    return JsonResponse(context, safe = False)

def get_sale_points(request):
    print('delete_all', request.GET.get('delete_all'))
    if request.GET.get('delete_all')=='true':
        SalePoint.objects.all().delete()
        return JsonResponse({}, safe = False)        
    filter_dic = {
    'y__gt' : float(request.GET.get('y_min')) - 500,
    'x__gt' : float(request.GET.get('x_min')) - 500,
    'y__lt' : float(request.GET.get('y_max')) + 500,
    'x__lt' : float(request.GET.get('x_max')) + 500,
    }
    need_cols = ['x','y','revenue_pred_model1','revenue_pred_model2','cann']
    objects = SalePoint.objects.filter(**filter_dic).values().values_list(*need_cols)
    df = pd.DataFrame(list(objects),columns=need_cols)
    print(df)
    
    context = {
        'sale_points': list(df.T.to_dict().values()),
    }
    return JsonResponse(context, safe = False)

def get_pred_squares(request):
    side = 300
    max_squares = 40000
    filter_dic = {
    'y__gt' : float(request.GET.get('y_min')),
    'x__gt' : float(request.GET.get('x_min')),
    'y__lt' : float(request.GET.get('y_max')),
    'x__lt' : float(request.GET.get('x_max')),
    'foot__isnull' : False,
    }
    objects = TimeSquare.objects.filter(**filter_dic)
    need_cols = ['x','y','foot']
    count = objects.count()
    if count>max_squares:
        df = pd.DataFrame()
    else:
        
        df = pd.DataFrame(list(objects.values().values_list(*need_cols)))
        df.columns = need_cols
        min_side_boared = 2000000
        if count<=min_side_boared:
            side_mult = 1
        else:
            side_mult = 2**int(math.log2(count/min_side_boared)**0.5)
        if side_mult!=1:
            side = side_mult*side
            agg = {'foot':'mean'}
            df['x'] = df['x'].apply(lambda x: round(x/side)*side)
            df['y'] = df['y'].apply(lambda x: round(x/side)*side)
            df = df.groupby(['x','y']).agg(agg).reset_index()
            df['foot'] = df['foot'].astype(int)
            #df['revenue_pred_model2'] = df['revenue_pred_model2'].astype(int)
            
        
        
    print('side', side)
    context = {
        'pred_squares': list(df.T.to_dict().values()),
        'half_side':side/2,
    }
    return JsonResponse(context, safe = False)    
    
def add3857(row):
    xy = transform(PROJ4326, PROJ3857, row['lon'], row['lat'])
    return xy
    
def get_clusters(df, n_clusters, agg, mode):
    if len(df)==0:
        return pd.DataFrame()
    if 'x' not in df.columns:
        df['xy'] = df.apply(add3857, axis = 1)
        df['x'] = df['xy'].apply(lambda xy:xy[0])
        df['y'] = df['xy'].apply(lambda xy:xy[1])
        df = df.drop(['xy','lat','lon'], axis = 1)

    xy = ['x','y']
    
    if n_clusters < len(df):
        if mode == 'clever':
        
            agg['x'] = 'size'
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[xy])
            df['cluster_label'] = (kmeans.labels_)

            df_clusters = df.groupby('cluster_label').agg(agg).reset_index()
            df_clusters = df_clusters.reset_index()
            df_clusters = df_clusters.rename(columns = {'x':'count'})
            df_clusters['is_one'] = df_clusters['count']!=1
            df_cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns = xy)
            df_cluster_centers['cluster_label'] = df_cluster_centers.index
            df_clusters = pd.merge(df_clusters, df_cluster_centers, on = 'cluster_label')
            df_clusters.drop('cluster_label', axis=1, inplace=True)
        elif mode=='stupid':

            delta_x = df['x'].max() - df['x'].min()
            delta_y = df['y'].max() - df['y'].min()
            square_side = (delta_x*delta_y/n_clusters)**0.5
            #print(df)
            df['x_round'] = df['x'].apply(lambda x: square_side*round(x/square_side))
            df['y_round'] = df['y'].apply(lambda x: square_side*round(x/square_side))

            agg['address'] = 'size'
            agg['x'] = 'mean'
            agg['y'] = 'mean'
            df_clusters = df.groupby(['x_round','y_round']).agg(agg).rename(columns={'address':'count'}).reset_index()
            df_clusters['is_one'] = df_clusters['count']==1
            df_clusters = df_clusters.reindex()
        else:
            assert False, 'Incorrect cluster mode'
        
    else:
        df_clusters = df[xy+list(agg.keys())]
        df_clusters['count'] = 1
        df_clusters['is_one'] = True
        for key in agg.keys():
            if agg[key]=='size':
                df_clusters[key] = 1
                break
    return df_clusters

def calc_place(row,x,y,nat_class):

    nearest_nat_classes_euclid = row['nearest_nat_classes_euclid']
    dic = json.loads(nearest_nat_classes_euclid)
    distances = np.array(dic[nat_class])
    R = ((x - row['x'])**2 + (y - row['y'])**2)**0.5
    place = sum(distances<R) + 1

    return place

def get_place_features(x,y):
    half_side = 5000
    nat_class = 'Магазин бытовой техники и электроники'
    filter_dic = {
                'x__gt' : float(x) - half_side,
                'y__gt' : float(y) - half_side,
                'x__lt' : float(x) + half_side,
                'y__lt' : float(y) + half_side,
    }
    
    features = ['flat_num', 'x', 'y', 'nearest_nat_classes_euclid']
    objects = House.objects.filter(**filter_dic).values().values_list(*features)
    df = pd.DataFrame(list(objects.values()), columns=features)
    if len(df)==0:
        return {}

    df['place'] = df.apply(lambda row: calc_place(row, float(x), float(y), nat_class), axis=1)
    
    gb = df.groupby('place')['flat_num'].sum()
    features_dic = {}
    places = range(1,12)
    for place in places:
        
        values = gb[gb.index==place]
        if len(values)==0:
            value = 0
        else:    
            value = values.iloc[0]
        features_dic[nat_class +'_'+ str(place)] = value

    return features_dic

def calc_isocrone(request):

    x = float(request.GET.get('x')) 
    y = float(request.GET.get('y')) 
   
    return features_dic

def get_cann_dict(x,y):
    half_side = 5e4
    influence_mult = 2
    our_brands = ['Ригла','Живика','Будь здоров']
    filter_dic = {
                'x__gt' : x - half_side,
                'y__gt' : y - half_side,
                'x__lt' : x + half_side,
                'y__lt' : y + half_side,
                'nat_class' : 'Аптека',
    }

    objects = OrganizationNatClass.objects.filter(**filter_dic).values()
    df_orgs = pd.DataFrame(list(objects))
    df_orgs['R'] = ((df_orgs['x'] - x)**2 + (df_orgs['y'] - y)**2)**0.5
    N = 5
    df_we_sorted = df_orgs[df_orgs['chain_name'].isin(our_brands)].sort_values('R').iloc[:N]
    dics = []
    for i, row in df_we_sorted.iterrows():
        dic = {}
        dic['R'] = row['R']
        dic['address'] = row['address']
        dic['chain_name'] = row['chain_name']
        R_boarder = row['R']

        n_comp = (    df_orgs['R'].min()/df_orgs[df_orgs['R']<=(influence_mult*R_boarder)]['R']   ).sum()

        dic['cannib'] = n_comp/(1+n_comp)
        dics.append(dic)
    return dics

def get_comp_dict(x,y):
    half_side = 5e4
    our_brands = ['Ригла','Живика','Будь здоров']
    filter_dic = {
                'x__gt' : x - half_side,
                'y__gt' : y - half_side,
                'x__lt' : x + half_side,
                'y__lt' : y + half_side,
                'nat_class' : 'Аптека',
    }

    objects = OrganizationNatClass.objects.filter(**filter_dic).values()
    df_orgs = pd.DataFrame(list(objects))
    df_orgs['R'] = ((df_orgs['x'] - x)**2 + (df_orgs['y'] - y)**2)**0.5
    N = 4
    df_orgs = df_orgs[df_orgs['chain_name'].isin(our_brands)].sort_values('R').iloc[:N+1]
    
    dics = []
    R_boarder = df_orgs['R'].iloc[-1]
    for i, row in df_orgs.iloc[:N].iterrows():
        dic = {}
        dic['R'] = row['R']
        dic['address'] = row['address']
        dic['chain_name'] = row['chain_name']

        dic['cannib'] = (row['R']/R_boarder)/2 + 0.5
        dics.append(dic)
    return dics

def get_time_3000(lon, lat, coords, root_url):
    page_url = root_url + '{},{};'.format(lon, lat)
    times = []
    for coord in coords:
        page_url = page_url + '{},{};'.format(coord[0], coord[1])
    page_url = page_url[:-1] + '?sources=0'
    page = requests.get(page_url)
    data = page.json()
    if 'durations' in data:
        times.extend(data['durations'][0][1:])
    else:
        print('no key name duration in data from osrm')
        times.extend([0]*len(coords))
    return times
def get_time(lon, lat, coords, mode):
    try:
        # Проверка на Питер
        if lat > 58 and lat > 58:
            root_url = {
                'driving': SERVER_URL_PETER_DRIVING,
                'foot': SERVER_URL_PETER_FOOT,
                }[mode]
        else:
            root_url = {
                'driving': SERVER_URL_MSK_DRIVING,
                'foot': SERVER_URL_MSK_FOOT,
                }[mode]
    except KeyError as e:
        raise ValueError('Undefined mode: {}'.format())
    times = []
    if len(coords) < 3000:
        times.extend(get_time_3000(lon,lat, coords, root_url))
    else:
        for coord_chunk in tqdm(np.array_split(coords, len(coords) / 3000)):
            times.extend(get_time_3000(lon, lat, coord_chunk, root_url))

    # Заменить все None на нули
    times = [0 if i is None else i for i in times]
    return times

def get_coord_time(x, y, step, rmax, mode):
    coords = get_coords(x, y, step, rmax)
    lat, lon = transform(PROJ3857, PROJ4326, x, y)
    times = get_time(lon, lat, coords, mode)
    return coords, times

def get_coords(x, y, step, rmax):
    coords = itertools.product(np.arange(x - rmax, x + rmax, step),np.arange(y - rmax, y + rmax, step))
    coords = list(coords)
    #print(len(list(coords)))
    #print(list(coords)[0])
    coords = list(map(lambda coord: transform(PROJ3857, PROJ4326, coord[0], coord[1]), coords))
    #print(coords)
    return coords

def brand_map(lat_min, lon_min, lat_max, lon_max, nat_classes, distance_name, filter_geo):
    xy = ['x','y']
    unq = ['source_id1','source_id2','source_name1','source_name2']

    columns = ['source_id','source_name','nat_class','chain_name','address']#nat_class just for fi
    filter_dic = filter_geo.copy()
    filter_dic['nat_class__in'] = nat_classes
    df_orgs = pd.DataFrame(list(OrganizationNatClass.objects.filter(**filter_dic).values().values_list(*columns)),
                           columns=columns)

    orgs_ids = df_orgs['source_id'].values
    df_orgs = df_orgs.set_index(['source_id', 'source_name'])

    columns = ['source_id','source_name','flat_num','x','y']

    df_homes = pd.DataFrame(list(House.objects.filter(**filter_geo).values().values_list(*columns)),columns=columns)
    home_ids = df_homes['source_id'].values
    df_homes = df_homes.set_index(['source_id', 'source_name'])

    q1 = Distance.objects.filter(
        source_id1__in=orgs_ids,
        source_name1='yandex_api',

        source_id2__in=home_ids,
        source_name2='reformagkh',
    )

    q2 = q1.values(*['source_id2','source_name2']).annotate(**{distance_name : Min(distance_name)})
    df2 = pd.DataFrame(list(q2))
    df1 = pd.DataFrame(list(q1.values(
        *['source_id2', 'source_name2', distance_name, 'source_id1', 'source_name1'])))

    df1 = df1.set_index([distance_name,'source_id2','source_name2'])

    q_orgs = OrganizationNatClass.objects.filter(source_id__in=orgs_ids,
        source_name='yandex_api').values()

    dics = []
    for i, row in tqdm(df2.iterrows()):
        el = row.to_dict()
        ind_values = [el['source_id2'],el['source_name2'],el[distance_name]]
        dic_dist = df1.loc[ind_values].iloc[0].to_dict()

        dic_home = df_homes.loc[[el['source_id2'],el['source_name2']]].iloc[0].to_dict()
        dic_org = df_orgs.loc[[dic_dist['source_id1'],dic_dist['source_name1']]].iloc[0].to_dict()
        dics.append({**el, **dic_dist, **dic_home, **dic_org})

    df = pd.DataFrame(dics)
    
    agg = {}
    agg['chain_name'] = lambda x: list(x)[0] if len(x)!=0 else '-'
    agg['x'] = lambda x: list(x)[0] if len(x)!=0 else '-'
    agg['y'] = lambda x: list(x)[0] if len(x)!=0 else '-'
    agg['flat_num'] = sum
    
    df_orgs = df.groupby(['source_name1','source_id1'],as_index=False).agg(agg)
    return df, df_orgs