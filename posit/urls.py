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
from claims.views import ClaimListView
from claims.views import ClaimListView
import userProfiles.regbackend

urlpatterns = [
    url(r'^$', 'posit.views.home', name='home'),
    url(r'^about/$', 'posit.views.about', name='about'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^claims/contribute/$', 'claims.views.addClaim', name='contributeClaim'),
    url(r'^claims/$', ClaimListView.as_view(), name='browseClaims'),
    url(r'^claims/(?P<claim_id>[0-9]{1,10})/', 'claims.views.viewClaim', name='viewClaim'),
    url(r'^meta/$', 'posit.views.meta', name='meta'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)