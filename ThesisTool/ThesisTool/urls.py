from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ThesisTool.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^',include('CheckingTool.urls')),
    #(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_URL}),

    #url(r'^admin/', include(admin.site.urls)),
)
