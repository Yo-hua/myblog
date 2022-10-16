from django.contrib import admin
from django.contrib.admin.models import LogEntry

from myblog.custom_site import custom_site
# 自定义管理后台

from blog.adminforms import PostAdminForm
from .models import Post, Category, Tag
from myblog.base_admin import BaseOwnerAdmin

from django.urls import reverse
from django.utils.html import format_html


# Register your models here.

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user',
                    'change_message']


class PostInline(admin.TabularInline):
    '''在分类界面实现可编辑'''
    fields = ("title", "desc", 'status')
    extra = 2  # 控制额外多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    search_fields = ['name']

    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def __str__(self):
        return self.name


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('id','name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    search_fields = ['name']
    list_display_links = ['name']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOnlyOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器 只展示当前用户的分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title', 'status', 'category', 'get_tags','operator', 'owner')
    list_filter = [CategoryOnlyOwnerFilter]
    search_fields = ['title', 'status', 'category__name']

    exclude = ('owner',)
    actions_on_top = True

    form = PostAdminForm

    # #为多余
    # actions_on_bottom = True
    # # 编辑页面
    # save_on_top = True

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category', 'status'),
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tags',)
        })
    )
    # filter_horizontal = ('tags',)

    # 获取多对多的tag显示
    def get_tags(self,instance):
        return [tag.name for tag in instance.tags.all()]

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'


    def __str__(self):
        return self.name


