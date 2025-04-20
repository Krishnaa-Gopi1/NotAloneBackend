from django.urls import path
from .views import hello_world , get_news
from .views import ScrapeNewsAPIView
urlpatterns = [
    path('hello/', hello_world),
    path('get_news/', ScrapeNewsAPIView.as_view(), name="scrape-news"),
    path('get_news/<str:topic>',get_news), 
]
