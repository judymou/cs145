from django.conf.urls import patterns, include, url
from mysite import settings
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    ('^hello/$', views.hello),
    ('^time/$', views.current_datetime),
    ('^welcome/$', views.product),
    ('^mypage/$', views.mypage),
    ('^lost/$', views.lost),
    ('^accounts/profile/$', views.mypage),
    ('^users/.*$', views.mypage),
    ('^tag/(.+)', views.display_tags),
    ('^product/(.+)', views.my_product),
    ('^accounts/', include('registration.backends.default.urls')),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # testin
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
        {'document_root':     settings.MEDIA_ROOT}),
)
