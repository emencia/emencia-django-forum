# -*- coding: utf-8 -*-
"""
Urls

TODO: Exclude "create" word for category slugs
"""
from django.conf.urls.defaults import *

from forum.views.index import IndexView
from forum.views.category import CategoryDetailsView, CategoryCreateView, CategoryEditView
from forum.views.post import PostEditView, PostDeleteView
from forum.views.thread import LastThreadViews, ThreadDetailsView, ThreadCreateView, ThreadEditView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="forum-index"),
    
    url(r'^last/$', LastThreadViews.as_view(), name="forum-thread-recent"),
    
    url(r'^category/create/$', CategoryCreateView.as_view(), name="forum-category-create"),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailsView.as_view(), name="forum-category-details"),
    url(r'^category/(?P<slug>[-\w]+)/edit/$', CategoryEditView.as_view(), name="forum-category-edit"),
    
    url(r'^category/(?P<category_slug>[-\w]+)/create/$', ThreadCreateView.as_view(), name="forum-thread-create"),
    url(r'^category/(?P<category_slug>[-\w]+)/(?P<thread_id>\d+)/$', ThreadDetailsView.as_view(), name="forum-thread-details"),
    url(r'^category/(?P<category_slug>[-\w]+)/(?P<thread_id>\d+)/edit/$', ThreadEditView.as_view(), name="forum-thread-edit"),
    url(r'^category/(?P<category_slug>[-\w]+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/edit/$', PostEditView.as_view(), name="forum-post-edit"),
    url(r'^category/(?P<category_slug>[-\w]+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/delete/$', PostDeleteView.as_view(), name="forum-post-delete"),
)
