from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hide_code', views.hideCodeKeys, name='hide_code'),
]