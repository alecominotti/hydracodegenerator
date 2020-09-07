from django.urls import path
from . import views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pepe', views.asd, name='index2'),
]