from django.db import models
from users.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


'''
Category: 文章分类
Tag：文章标签
Post: 发表的文章
'''

class Category(models.Model):
    '''文章的分类'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    '''发表的文章'''
    title = models.CharField(max_length=70)  # 文章标题
    body = models.TextField()  # 文章正文
    created_time = models.DateTimeField()  # 创建时间
    modified_time = models.DateTimeField()  # 最后一次修改时间
    excerpt = models.CharField(max_length=200, blank=True)  # 文章概要
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 所属分类
    tags = models.ManyToManyField(Tag, blank=True)  # 标签
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 作者
    views = models.PositiveIntegerField(default=0, blank=True)  # 阅读量

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 使文章阅读量自动+1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写父类的save()方法，使当用户没有填写文章概要的时候自动生成概要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md_post = markdown.Markdown(extras=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md_post.convert(self.body))[:90]
        super(Post, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-created_time']
