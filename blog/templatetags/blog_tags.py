from ..models import Post, Tag, Category
from django import template
from django.db.models.aggregates import Count


register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    '''获取最近发布文章'''
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    '''按时间归档模板标签'''
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_category():
    '''分类模板标签'''
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    '''标签模板标签'''
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)