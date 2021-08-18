from django.urls import path
from .views import *


urlpatterns = [
    path('', BaseListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('article/', ArticleListView.as_view(), name='article'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
]