#from django.conf.urls import urls

from . import views
from django.urls import path

 
urlpatterns = [
    path('', views.index, name='index'),
]

