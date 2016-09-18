from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from claims import views


# API endpoints

urlpatterns = format_suffix_patterns([
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^claims/$', views.claim_list),
    url(r'^claims/(?P<pk>[0-9]+)/$', views.claim_detail),
    url(r'^affirmations/$', views.affirmation_list),
    url(r'^affirmations/(?P<pk>[0-9]+)/$', views.affirmation_detail),
])


# Login and logout views for the browsable API

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
