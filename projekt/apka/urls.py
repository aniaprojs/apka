from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('generate-image/', views.generate_image, name='generate_image'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
