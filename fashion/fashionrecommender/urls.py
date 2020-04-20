from django.urls import path

from . import views

app_name = 'fashion'

urlpatterns = [
    path('', views.index, name='index'),
    path('capture', views.capture, name='capture'),
    path('upload', views.upload, name='upload'),
    path('runmodel', views.runmodel, name='runmodel'),
]
