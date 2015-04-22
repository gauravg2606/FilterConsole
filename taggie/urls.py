__author__ = 'patley'
from django.conf.urls import patterns, url


from taggie import views

urlpatterns =patterns("",
            url(r'^$',views.index, name='index'),
            url(r'(?P<sticker_id>\d+)/$', views.details ,name='details'),
            url(r'(?P<sticker_id>\d+)/results/$', views.results, name='results'),
            url(r'(?P<sticker_id>\d+)/vote/$', views.vote, name='vote'),
            url(r'(?P<sticker_id>\d+)/add/$', views.add, name='add'),
            url(r'(?P<catid>.*)/category/$', views.category, name='category'),
            url(r'^categories/$', views.cat_list, name='cat_list'),


)

