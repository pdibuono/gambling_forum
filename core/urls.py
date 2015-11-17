from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
     url(r'^$', Home.as_view(), name='home'),
     url(r'^user/', include('registration.backends.simple.urls')),
     url(r'^user/', include('django.contrib.auth.urls')),
     url(r'^pick/create/$', login_required(PickCreateView.as_view()), name='pick_create'),
     url(r'pick/$', login_required(PickListView.as_view()), name='pick_list'),
     url(r'pick/(?P<pk>\d+)/$', login_required(PickDetailView.as_view()), name='pick_detail'),
     url(r'^pick/update/(?P<pk>\d+)/$', login_required(PickUpdateView.as_view()), name='pick_update'),
     url(r'^pick/delete/(?P<pk>\d+)/$', login_required(PickDeleteView.as_view()), name='pick_delete'),
     url(r'^pick/(?P<pk>\d+)/reply/create/$', login_required(ReplyCreateView.as_view()), name='reply_create'),
     url(r'^pick/(?P<pick_pk>\d+)/reply/update/(?P<reply_pk>\d+)/$', login_required(ReplyUpdateView.as_view()), name='reply_update'),
     url(r'^pick/(?P<pick_pk>\d+)/reply/delete/(?P<reply_pk>\d+)/$', login_required(ReplyDeleteView.as_view()), name='reply_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
)
