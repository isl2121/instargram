from django.urls import path, include
from . import views

app_name = 'app'
urlpatterns = [
    path('main', views.main, name="main"),
    path('', views.MainLv.as_view(), name="index"),
    path('app/comment_new/', views.comment_new, name="comment_new"),
    path('app/comment_del/', views.comment_del, name="comment_del"),
    path('app/like_change/', views.like_chage, name="like_change"),
    path('make_app/', views.MakeApp.as_view(), name="make_app"),
    path('modify_app/<int:pk>', views.Modifyapp.as_view(), name="modify_app"),
    path('delete_app/<int:pk>', views.Deleteapp.as_view(), name="delete_app"),
    path('app/tags/<str:tag>/', views.MainLv.as_view(), name="get_tag"),
    path('app/<str:username>/list/', views.MainLv.as_view(), name="user_app_list"),
    path('follow/list', views.MainLv.as_view(), name="follow_user"),
    path('user/<str:username>/list', views.get_list, name="user_list"),

]