from django.urls import path
from app.views import *
urlpatterns = [
    path('', homepage, name="home"),
    path('about',about, name="about"),
    path('contact',hello, name="contact"),
    path('blogs',blogs,name="blogs"),
    path('read/<str:id>', read, name="read"),
    path('delete/<str:id>', delete, name="delete"),
    path('create', create,name="create"),
    path('edit/<str:id>',edit,name="edit"),
    path('signup',signup,name="signup"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
]
