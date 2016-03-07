from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    
    #url(r'^', include('qa.urls'))  - other way - in another file
    
    url(r'^$', 'qa.views.test', name='index'),
    url(r'^login/.*$', 'qa.views.test', name='login'),
    url(r'^signup/.*$', 'qa.views.test', name='signup'),
    url(r'^question/\w+/.*$', 'qa.views.test', name='question'),
    url(r'^ask/.*$', 'qa.views.test', name='ask'),
    url(r'^popular/.*$', 'qa.views.test', name='popular'),
    url(r'^new/.*$', 'qa.views.test', name='new')
)

