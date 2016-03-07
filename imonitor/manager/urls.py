from django.conf.urls import patterns, include, url
from django.contrib import admin
from manager.views import * 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views


urlpatterns = patterns('',    	
    url(r'^d/$','manager.views.department_detail', name='department_detail'),
 
)
