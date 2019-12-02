from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib import admin
from django.utils.text import slugify

app_name = "posts"

urlpatterns = [
    path('/posts',views.posts,name = "posts"),
    path('',views.posts_list, name = "list"),
    path('update/<slug:slug>',views.post_update, name = "update"),
    path('create/',views.post_create, name = "create"),
    path('delete/<slug:slug>', views.post_delete, name = "delete"),
    path('krallar/<slug:slug>',views.krallar, name = "krallar"),
    path('detail/<slug:slug>',views.detail, name = "detail"),
    path('add_comment/<slug:slug>',views.add_comment, name = "add_comment"),
    path('get_child_comment_form/',views.get_child_form, name = "get_child_comment_form"),
    path('new_add_comment/<int:pk>/<str:model_type>',views.new_add_comment, name = "new_add_comment"),
    path('post_favorite_users/<slug:slug>',views.post_list_favorite_user, name = "post_list_favorite_user"),
    path('add_remove_favorite/<slug:slug>',views.add_or_remove_favorite, name = "add_remove_favorite"),


]