from django.urls import path
# from django.conf.urls import url
from weather import views

urlpatterns = [
    path('', views.index, name="home"),
    path('notification/', views.indexNotification, name="notification"),
    path('configuration/', views.indexConfiguration, name="configuration"),
    path('validation/', views.IdealWeight)
]
