from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Post, Tag
from .models import Category


# Create your views here.


def post_list(requset, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.lates_post()
    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
    }
    return render(requset, 'blog/list.html', context=context)


def post_detail(requset, article_name=None):
    try:
        post = Post.objects.get(title=article_name)
    except Post.DoesNotExist:
        post = None
    return render(requset, 'blog/detail.html', context={'post': post})
