from django.urls import path
from news import views
from news.views import scrape


urlpatterns = [
    path('categories/', views.categories, name="categories"),
    path('about/', views.about, name="about"),
    path('bi/', views.bi, name="bi"),
    path('prog/', views.prog, name="prog"),
    path('robotics/', views.robotics, name="robotics"),
    path('crypto/', views.crypto, name="crypto"),
    path('scrape/', scrape, name="scrape"),
    path('', views.index, name="index")
]