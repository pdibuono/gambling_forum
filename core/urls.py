from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
     url(r'^$', Home.as_view(), name='home'),
     url(r'^user/', include('registration.backends.simple.urls')),
     url(r'^user/', include('django.contrib.auth.urls')),
     url(r'^pick/create/$', PickCreateView.as_view(), name='pick_create'),
     url(r'pick/$', PickListView.as_view(), name='pick_list'),
     url(r'pick/(?P<pk>\d+)/$', PickDetailView.as_view(), name='pick_detail'),
     url(r'^pick/update/(?P<pk>\d+)/$', PickUpdateView.as_view(), name='pick_update'),
     url(r'^pick/delete/(?P<pk>\d+)/$', PickDeleteView.as_view(), name='pick_delete'),
     url(r'^pick/(?P<pk>\d+)/reply/create/$', ReplyCreateView.as_view(), name='reply_create'),
     url(r'^pick/(?P<pick_pk>\d+)/reply/update/(?P<reply_pk>\d+)/$', ReplyUpdateView.as_view(), name='reply_update'),                 
)
