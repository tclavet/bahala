from django.conf.urls import url, include
from landing_page import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
]
