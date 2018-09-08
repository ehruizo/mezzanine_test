from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test1, name='test1'),
    url(r'^test/(?P<par1>[^/]+)/(?P<par2>[^/]+)/$', views.test2, name='test2'),
    url(r'^testform/$', views.test3, name='test3'),
    url(r'^user/(?P<userid>[0-9]+)/$', views.user_invoice, name='userinv'),
    url(r'^invoice/(?P<invid>[0-9]+)/$', views.invoice_details, name='invdetails'),
    url(r'^invoice/(?P<invid>[0-9]+)/delete$', views.delete_product, name='delprodinv'),
    url(r'^user/(?P<userid>[0-9]+)/newinvoice/$', views.new_invoice, name='newinvoice'),
    url(r'^newuser/$', views.new_user, name='newuser'),
    url(r'^analytics/$', views.model_scorer, name='analytics'),
    url(r'^bi/$', views.google_chart, name='bi'),
]
