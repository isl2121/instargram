from django.urls import path, include
from . import views

app_name = 'app'
urlpatterns = [
    path('main', views.main, name="main"),
    path('', views.MainLv.as_view(), name="index"),
]