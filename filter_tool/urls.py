from django.conf.urls import url
from filter_tool import views

urlpatterns = [
    url(r'^$', views.FilterUpload.as_view(), name='Filter Upload'), # Notice the URL has been named
    url(r'^launch$',views.launch,name="Launch"),
    url(r'^order/$',views.orderForm,name="OrderPage"),
    url(r'^orderUpdate/$',views.orderUpdate,name="OrderUpdate"),
    # url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^upload_asset/$',views.upload_asset),
]