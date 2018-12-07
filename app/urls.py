from django.urls import path, include
from . import views

app_name = 'app'
urlpatterns = [
    path('main', views.main, name="main"),
    path('', views.MainLv.as_view(), name="index"),
    path('app/comment_new/', views.comment_new, name="comment_new"),
    path('app/comment_del/', views.comment_del, name="comment_del"),
    path('app/like_change/', views.like_chage, name="like_change2"),
    path('app/make_app/', views.MakeApp.as_view(), name="make_app"),
]