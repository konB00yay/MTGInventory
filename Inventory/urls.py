from django.urls import path

from . import views

urlpatterns = [
    path('', views.CardTableView.as_view()),
    path('upload/', views.upload, name='upload'),
]