from django.urls import path, include

from . import views

app_name = 'carbike'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
]