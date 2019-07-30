from django.contrib.syndication.views import Feed
from .models import Post

class AllPostRssFeed(Feed):
    title = "Django 博客RSS订阅演示"  # 显示在阅读聚合器上的标题

    link = "/"  # 通过聚合阅读器转到网站的地址

    # 显示在聚合阅读器上的描述信息
    description_template = "Django 博客教程演示项目测试文章"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return "[%s]%s" % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body