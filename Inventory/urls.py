from django.urls import path

from . import views

urlpatterns = [
    path('', views.CardTableView.as_view(), name='card'),
    path('upload/', views.SoldTableView.as_view(), name='upload'),
    path('market/', views.MarketAnalysis.as_view(), name='market')
]