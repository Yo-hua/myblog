from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def links(request,example=None):
    content='the links example={example}'.format(example=example)
    return HttpResponse(content)

def example_res(request,example=None):
    if example:
        print('example exit %s',example)
        content='the example_res={example}'.format(example=example)
        return HttpResponse(content)
    return HttpResponse('example NOT exit')
