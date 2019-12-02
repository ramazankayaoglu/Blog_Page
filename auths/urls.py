from django.conf.urls import url
from .views import register,user_login
from django.urls import path,include
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from auths import views


app_name = "auths"

urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.user_login,name = "login"),
    path('logout/',views.user_logout,name = "logout"),
    path('settings/',views.user_settings,name = "settings"),
    path('user_profile/<str:username>/about/',views.user_about, name="about"),
    path('user_profile/<str:username>/',views.user_profile, name="user_profile"),
    path('password_change/',views.user_password_change,name ="password_change"),

]