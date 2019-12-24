from django.urls import include, path

urlpatterns = [
    path('lentti/', include('geofencing.urls')),
]
