from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib import admin

app_name = "following"


urlpatterns = [
        path('takiplesme_sistemi/',views.kullanici_takip_et_cikar,name="kullanici_takip_et_cikar"),
        path('post_fav_user_takip_et_cikar/',views.kullanici_takip_et_cikar_for_post,name="post_fav_user_takip_et_cikar"),
        path('modal_takip_et_cikar/',views.kullanici_modal_takip_et_cikar,name="modal_takip_et_cikar"),
        path('ramo/', views.ramo, name = "ramo"),
        path('followed_or_followers_list/<str:follow_type>/', views.followed_or_followers_list, name = "followed_or_followers_list"),

]