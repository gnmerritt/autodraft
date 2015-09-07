from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from draftHost import views, api

urlpatterns = patterns(
    'draftHost.views',
    url(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.html',
                             content_type='text/plain')),
    url(r'^my_team/(?P<key>[^/]+)/?$', views.my_team, name='my_team'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^mock_draft/?$', views.mock_draft, name='mock_draft'),
    url(r'^doc/$', views.documentation, name='documentation'),
    url(r'^draft/(?P<id>\d+)/?$', views.draft_detail, name='draft'),
    url(r'^draft/(?P<id>\d+)/picks/?$', views.draft_pick_ajax,
        name='pick_ajax'),
    url(r'^draft/(?P<id>\d+)/results/?$', views.draft_results, name="results"),
    url(r'^/?$', views.index, name='index'),
    url(r'^error/?$', views.reg_error, name='error'),

    # API v1
    url(r'^api/v1/', include(api, namespace="api"))
)
