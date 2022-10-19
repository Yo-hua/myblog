from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()

# 绑定自定义模板层中的tag
@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }
