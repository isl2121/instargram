from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.SignupUserView.as_view(), name="signup"),
    path('signup_done', views.RegisteredView.as_view(), name='signup_done'),
    path('set/follow/', views.set_follow, name="set_follow"),
    path('update_profile', views.Update_profile, name="update_profile"),
    path('update_password', views.Update_passwd, name="update_password"),
]
