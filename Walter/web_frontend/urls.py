from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^history/', views.history, name='history'),
    url(r'^insert/', views.insert, name='insert')
]
