from django.conf.urls import patterns, include, url
from django.contrib import admin

from taggie import views as tviews
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StickerTagger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', tviews.index, name = 'index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tag/',include('taggie.urls'),name="tag"),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
