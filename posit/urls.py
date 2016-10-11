"""posit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from posit import views as posit_views
from claims.models import Affirmation
from claims import views as claims_views
from rest_framework import routers, serializers, viewsets  # for REST API thing
# import userProfiles.regbackend


urlpatterns = [
    # Homepage
    url(r'^$', posit_views.home, kwargs=None, name='home'),
    # About and Meta pages
    url(r'^about/$', posit_views.about, kwargs=None, name='about'),
    url(r'^meta/$', posit_views.meta, kwargs=None, name='meta'),
    # Account-related URLs for Django-Registration-Redux
    url(r'^accounts/', include('registration.backends.default.urls')),
    # claims
    url(r'^claims/contribute/$', claims_views.addClaim, kwargs=None, name='contributeClaim'),
    url(r'^claims/$', claims_views.ClaimListView.as_view(), kwargs=None, name='browseClaims'),
    url(r'^claims/(?P<claim>[0-9]{1,10})/', claims_views.viewClaim, kwargs=None, name='viewClaim'),
    # arguments
    url(r'^arguments/contribute/$', claims_views.addArgument, kwargs=None, name='contributeArgument'),
    url(r'^arguments/$', claims_views.ArgumentListView.as_view(), kwargs=None, name='browseArguments'),
    url(r'^arguments/(?P<argument>[0-9]{1,10})/', claims_views.viewArgument, kwargs=None, name='viewArgument'),
    # urls for the REST API
    url(r'^api/', include('claims.urls')),
    # Admin-related URLs (including Grappelli)
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls, kwargs=None, name=None),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
