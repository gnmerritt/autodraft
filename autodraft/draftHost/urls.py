from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from draftHost import views, api

urlpatterns = patterns('draftHost.views',
    url(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.html', content_type='text/plain')),
    # HTML views
    url(r'^my_team/(?P<key>[^/]+)/?$', views.my_team, name='my_team'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^doc/$', views.documentation, name='documentation'),
    url(r'^/?$', views.draft_page, name='draft_page'),

    # API v1
    url(r'^api/v1/', include(api, namespace="api"))
)
