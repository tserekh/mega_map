from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include, url
from main_map import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('main_map/', include('main_map.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
  
]