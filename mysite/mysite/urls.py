from django.conf.urls import patterns, include, url
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
    ('^accounts/', include('registration.backends.simple.urls')),
    ('^product/$', views.enter_product),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
