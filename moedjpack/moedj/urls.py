from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.http import HttpResponse
from django.contrib.auth.views import login, logout

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loginSina/(\S+)/$', 'moedjpack.auth.views.loginSina'),
    url(r'^sinacallback/$', 'moedjpack.auth.views.sinacallback'),
    url(r'^re_auth_sina/$', 'moedjpack.auth.views.re_auth_sina'),
    url(r'^clean_auth/$', 'moedjpack.auth.views.clean_auth'),
    url(r'^$', 'moedjpack.moewiki.views.index'),
    url(r'^forbidden/$', 'moedjpack.moewiki.views.forbidden_proc'),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /",
        mimetype="text/plain")),
    url(r'^accounts/login/', login),
    url(r'^forbidden_item/(\S+)/$', 'moedjpack.moewiki.views.forbidden_item'),
    # url(r'^verify/', 'moewiki.views.verify')
)
