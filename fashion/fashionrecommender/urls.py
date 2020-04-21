from django.urls import path

from . import views

app_name = 'fashion'

urlpatterns = [
    path('', views.index, name='index'),
    path('capture', views.capture, name='capture'),
    path('upload', views.upload, name='upload'),
    path('runmodel', views.runmodel, name='runmodel'),
    path('search', views.search, name='search'),
    path('showsimilar', views.showsimilar, name='showsimilar'),
    path('lazyload', views.lazyload, name='lazyload'),
]
