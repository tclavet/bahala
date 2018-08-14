from django.conf.urls import url, include
from booking import views

urlpatterns = [
    url(r'^booking/$', views.booking, name='booking'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
]
