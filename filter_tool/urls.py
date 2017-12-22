from django.conf.urls import url
from filter_tool import views
from filter_tool import views2

urlpatterns = [
    url(r'^$', views.FilterUpload.as_view(), name='Filter Upload'), # Notice the URL has been named
    url(r'^launch$',views.launch,name="Launch"),
    url(r'^order/$',views.orderForm,name="OrderPage"),
    url(r'^orderUpdate/$',views.orderUpdate,name="OrderUpdate"),
    url(r'^upload_asset/$',views.upload_asset),

    url(r'^mrr$', views2.FilterUpload.as_view(), name='Filter2 Upload'), # Notice the URL has been named
    url(r'^categoryidupload$', views2.CategoryUpload.as_view(), name='CategoryUpload'),
    url(r'^launch2$',views2.launch,name="Launch2"),
    url(r'^categoryorder/$', views2.fetchCategoryOrderForm, name="CategoryOrderPage"),
    url(r'^assetfortype/$', views2.fetchAssetForm, name="FetchAssetPage"),
    url(r'^assetorder/$', views2.fetchAssetOrderForm, name="AssetOrderPage"),
     url(r'^deleteasset/$', views2.deleteAssetForm, name="DeleteAssetPage"),
    url(r'^categoryorderupdate/$', views2.categoryOrderUpdate, name="CategoryOrderUpdate"),
    url(r'^assetorderupdate/$', views2.assetOrderUpdate, name="AssetOrderUpdate"),
    url(r'^getcategoryfortype/$', views2.getCategoryForType, name="CategoryForType"),
    url(r'^upload_asset2/$',views2.upload_asset),
    url(r'^categoryimageupload/$', views2.categoryImageUpload, name="CategoryImage"),

]