from django.shortcuts import get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Post, Tag, Category
from config.models import SideBar

from django.views import View

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import ContextMixin

from django.db.models import Q,F

from comment.forms import CommentForm
from comment.models import Comment


# Create your views here.
class CommonViewMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        print(context)
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    ## Category 虽然已经自带此类方法 但是CommonViewMixin类还没有该方法
    def get_navs(self):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class IndexView(CommonViewMixin, ListView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL) \
        .select_related('owner') \
        .select_related('category') # 取model类
    #print(type(queryset))
    paginate_by = 3 # 明显来自ListView类
    context_object_name = 'post_list' # 来自ListView类 指定生成当前类的名字 产生新对象的名字
    template_name = 'blog/list.html'


'''
来自父类IndexView
CategoryView 已被指定context_object_name和template_name
'''
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 实际上是封装了类似get_by_category的效果
        category_id = self.kwargs.get('category_id')
        #  get_object_or_404 获取对象实例 否则返回404
        category = get_object_or_404(Category, pk=category_id)
        context.update(
            {'category': category}
        )
        #print('CategoryView happened')
        return context

    # get_queryset体现在context的数据集合
    def get_queryset(self):
        '''

        重写queryset,根据分类过滤 get_queryset属于ListView的
        '''
        queryset = super().get_queryset()
        # self.kwargs.get从URL里取值
        #print('CategoryView get_queryset happened')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

    def get_context_data_testing(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category_id')
        #  get_object_or_404 获取对象实例 否则返回404
        category = get_object_or_404(Category, pk=category_name)
        context.update(
            {'category': category}
        )
        return context

'''
来自父类IndexView
TagView 已被指定context_object_name和template_name
'''
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            tag_id = self.kwargs.get('tag_id')
            tags = get_object_or_404(Tag, pk=tag_id)
            context.update(
                {'tags': tags}
            )
        except Exception as e:
            raise e
            #print('未找到tag_id 发生错误：%s',e)
        #print('TagView happened')
        return context

    def get_queryset(self):
        ''' 重写queryset,根据分类过滤 get_queryset属于ListView的'''
        queryset = super().get_queryset().filter()
        # self.kwargs.get从URL里取值
        tag_id = self.kwargs.get('tag_id')
        #print('TagView get_queryset happened')
        return queryset.filter(tag_id=tag_id)

class PostDeatilView(CommonViewMixin, DetailView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # queryset = Post.lates_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    ## 已抽象评论模块的替代方法
    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommentForm,
    #         'comment_list':Comment.get_by_target(self.request.path)
    #     })
    #     return context

class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context.update({
                'keyword':self.request.GET.get('keyword','')
            }
        )
        #print('SearchView happened')
        return context

    def get_queryset(self):
        queryset=super().get_queryset()
        keyword=self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword)|Q(desc__icontains=keyword))

class AuthorView(IndexView):
    def get_queryset(self):
        queryset=super().get_queryset()
        author_id=self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context.update({
                'owner_id':self.request.GET.get('owner_id','')
            }
        )
        #print('AuthorView happened')
        return context

### 以下为前期测试使用可以忽略

### 以下为前期测试使用可以忽略
class MyView(View):

    def get(self, request):
        # <views logic>
        return HttpResponse('hand')

    def test_text(self):
        # <views logic>
        result = 'here is res '
        return HttpResponse(result)

class PostListViewTest(ListView):
    queryset = Post.latest_posts()
    paginate_by = 2
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class PostViewDetailTest(DetailView):
    # requirement 'model' and 'template_name'
    model = Post
    queryset = Post.objects.all()
    queryset = queryset
    template_name = 'articlebyDetailView.html'

def post_list(requset, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.hot_posts()
    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        'sidebars': SideBar.get_comment(),
    }
    # 更新使用 提取侧栏分类集合函数
    context.update(Category.get_navs())
    return render(requset, 'blog/list.html', context=context)

def post_detail(requset, article_name=None):
    try:
        post = Post.objects.get(title=article_name)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(requset, 'blog/detail.html', context={'post': post})
