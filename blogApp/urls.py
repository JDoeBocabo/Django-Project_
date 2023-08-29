
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('create/', views.addBlog, name="create"),
    path('register/', views.signUp, name="signUp"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('updateBlog/<slug>', views.updateBlog, name='updateBlog'),
    path('deleteBlog/<slug>', views.deleteBlog, name="deleteBlog"),
    path('blogs/<slug:slug>/', views.blogs, name="blogs"),
    path('search/', views.search, name="search"),
    path('delete-account/', views.deleteAccount, name='deleteAccount'),
    path('editProfile/<str:username>/', views.editProfile, name='editProfile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('changeProfilePicture/<str:username>/',
         views.changeProfilePicture, name='changeProfilePicture'),
]
