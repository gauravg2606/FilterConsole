from django.conf.urls import url
from sticker_tool import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^index/$', views.IndexPageView.as_view(), name='index'),
url(r'^testing/$', views.DropboxPageView.as_view(), name='testing')
    ]