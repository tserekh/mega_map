from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.urls import path, include
from . import views
from django.conf.urls import url


app_name = 'main_map'

urlpatterns = [
    path('', views.index, name='index'),
    #url(r'^', include('main_map.urls', namespace="orgs")),
    url(r'^get_metros/$', views.get_metros, name='get_metros'),
    url(r'^get_orgs/$', views.get_orgs, name='get_orgs'),
    url(r'^get_homes/$', views.get_homes, name='get_homes'),
    url(r'^get_polygons/$', views.get_polygons, name='get_polygons'),
    url(r'^get_lines/$', views.get_lines, name='get_lines'),
    url(r'^cacl_sale_point/$', views.cacl_sale_point, name='cacl_sale_point'),
    url(r'^get_sale_points/$', views.get_sale_points, name='get_sale_points'),
    
    url(r'^get_ground_stops/$', views.get_ground_stops, name='get_ground_stops'),
    url(r'^get_oper_squares/$', views.get_oper_squares, name='get_oper_squares'),
    url(r'^get_pred_squares/$', views.get_pred_squares, name='get_pred_squares'),   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += static(settings.MEDIA_URL,

# document_root=settings.MEDIA_ROOT)