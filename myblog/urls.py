"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from .custom_site import custom_site
from blog.views import post_list, post_detail
from config.views import links, example_res

from blog.views import (MyView, PostViewDetailTest, PostListViewTest, PostDeatilView,
                        IndexView, CategoryView, TagView)
from django.views.generic import TemplateView, ListView

urlpatterns = [
    re_path('^$', post_list),

    ### FOR TEST
    # re_path('^test_text/$', MyView.test_text),
    # re_path('^about_TemplateView/$', TemplateView.as_view(template_name='about_TemplateView.html')),
    # re_path('^articlebyDetailView/(?P<pk>\d+)$',PostViewDetailTest.as_view(),name='DetailView-TEST'),
    # re_path('^post_listbyListView/(?P<pk>\d+)$',PostListViewTest.as_view(),name='ListView-TEST'),
    ###

    re_path('^$', IndexView.as_view, name='index'),
    re_path('^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    re_path('^tags/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    re_path('^post/(?P<post_id>\d+)/$', PostDeatilView.as_view(), name='article-detail'),

    re_path('^links/$', links, {'example': 'nop'}, name='links'),
    re_path('^example_res/$', example_res, {'example': 'This is example'}, name='example_res'),

    path("admin/", admin.site.urls, name='admin'),
]
