from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from claims import views


# API endpoints

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^users/$', views.UserList.as_view(),name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),name='user-detail'),
    url(r'^claims/$', views.ClaimList.as_view(),name='claim-list'),
    url(r'^claims/(?P<pk>[0-9]+)/$', views.ClaimDetail.as_view(),name='claim-detail'),
    url(r'^affirmations/$', views.AffirmationList.as_view(),name='affirmation-list'),
    url(r'^affirmations/(?P<pk>[0-9]+)/$', views.AffirmationDetail.as_view(),name='affirmation-detail'),
])


# Login and logour views for the browsable API

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
