from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm
import markdown


# Create your views here.


def post_comment(request, post_pk, user_name):
    post = get_object_or_404(Post, pk = post_pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    # 判断使用的提交方法是否为POST
    if request.method == 'POST':
        # 利用POST方法提交的表单信息，构造CommentForm实例，生成Django表单
        form = CommentForm(request.POST)

        # 判断表单信息是否符合格式要求
        if form.is_valid():
            # 如果符合，则保存form数据
            # 1.利用表单数据生成Comment模型类实例，但还不保存到数据库(commit=False)
            comment = form.save(commit=False)
            # 2.将评论和被评论的文章关联起来，获取用户姓名和邮箱
            comment.post = post
            comment.name = user_name
            # 3.保存到数据库
            comment.save()

            # 重定向到post的详情页实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 如果表单信息不合法，则重新渲染详情页，并渲染表单的错误
            comment_list = post.comment_set.all()  # 这里是通过外键反向获取所有评论信息
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)
    # 如果非POST方法，表明用户没有输入表单信息（直接点了评论按钮）,则重定向文章详情页
    else:
        return redirect(post)
