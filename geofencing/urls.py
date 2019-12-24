from django.urls import path

from . import views

urlpatterns = [
    path('app', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('elastic-setup', views.elastic_setup, name='elastic-setup'),
    path('search', views.search, name='search'),
]