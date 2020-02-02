from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('elastic-setup', views.elastic_setup, name='elastic-setup'),
    path('search', views.search, name='search'),
]