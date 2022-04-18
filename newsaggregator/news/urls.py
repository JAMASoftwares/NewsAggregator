from django.urls import path
from news import views


urlpatterns = [
    path('categories/', views.categories, name="categories"),
    path('about/', views.about, name="about"),
    path('bi/', views.bi, name="bi"),
    path('prog/', views.prog, name="prog"),
    path('robotics/', views.robotics, name="robotics"),
    path('crypto/', views.crypto, name="crypto"),
    path('update/', views.update, name="update"),
    path('', views.index, name="index")
]