from django.db import models


# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)  # 评论人昵称
    email = models.EmailField(max_length=255, blank=True)  # 评论人邮箱
    url = models.URLField(blank=True)  # 评论人个人网站
    text = models.TextField()  # 评论主题信息
    created_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)  # 评论的文章

    def __str__(self):
        return self.text[:20]