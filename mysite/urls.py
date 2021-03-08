from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_map/', include('main_map.urls')),

    #url(r'^', include('main_map.urls', namespace="orgs")),
    #url(r'^get_metros/$', include('main_map.urls', namespace="orgs")),
    

    
    ]