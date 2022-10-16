from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link

# Create your views here.


def links(request,example=None):
    content='the links example={example}'.format(example=example)
    return HttpResponse(content)

# 直接传值
def example_res(request,example=None):
    if example:
        print('example exit %s',example)
        content='the example_res={example}'.format(example=example)
        return HttpResponse(content)
    return HttpResponse('example NOT exit')

class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'
