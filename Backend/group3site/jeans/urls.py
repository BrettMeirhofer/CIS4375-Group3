from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dd', views.dict3, name='datadictionary'),
]