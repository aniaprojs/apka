from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('generate-image/', views.generate_image, name='generate_image'),
    path('get_title/', views.get_title, name='get_title'),
    path('get_hashtags/', views.get_hashtags, name='get_hashtags'),
]
