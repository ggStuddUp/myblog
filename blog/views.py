from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def index(request):
#     '''博客首页'''
#     post_list = Post.objects.all()
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)

"""
def detail(request, pk):
    '''显示博客详情'''
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()  # 阅读量+1
    # post.body = markdown.markdown(post.body,
    #                               extension=[
    #                                     'markdown.extensions.extra',
    #                                     'markdown.extensions.codehilite',
    #                                     'markdown.extensions.toc',
    #                               ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    post.body = markdown2.markdown(post.body, extras=["fenced-code-blocks"])
    return render(request, 'blog/detail.html', context={'post': post,
                                                        'form': form,
                                                        'comment_list': comment_list})

def archives(request, year, month):
    '''按归档返回文章列表（按时间归档）'''
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    '''按分类返回文章列表'''
    post_list = Post.objects.filter(category__pk=pk)
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""


'''使用基于类的通用视图'''
from django.views.generic import ListView, DetailView


class IndexView(ListView):
    '''获取文章列表的通用类视图'''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        paginate_date = self.get_paginate_date(paginator, page, is_paginated)
        context.update(paginate_date)
        return context

    def get_paginate_date(self, paginator, page, is_paginated):
        '''获取自定义分页导航所需参数'''
        # 1 ... 4 5 [6] 7 8 ... 10
        if not is_paginated:
            return {}
        page_number = page.number  # 获取当前页
        total_pages = paginator.num_pages  # 获取总页数
        page_range = paginator.page_range  # 获取分页列表[1,2,3...]
        left = []  # 当前页左侧页显示页
        right = []  # 当前页右侧页显示页
        first = False  # 标志最左侧是否需要显示1
        last = False  # 标志最右侧是否需要显示总页数
        left_has_more = False  # 标志左侧是否需要显示省略号
        right_has_more = False  # 标志右侧是否需要显示省略号

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data



class CategoryView(IndexView):
    '''获取某分类的文章和类似获取文章列表，这里直接继承IndexView'''
    def get_queryset(self):
        '''重写ListView的get_queryset方法，原方法是获取全部.all()'''
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk')) # 通过url参数获取分类
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchiveView(IndexView):
    '''获取按时间归档的文章列表，同样继承IndexView'''
    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                              created_time__month=self.kwargs.get('month'))


class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(DetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 这里覆写的主要目的是获取文章的主体，并进行Markdown渲染
        post = super(DetailView, self).get_object(queryset=None)
        # post.body = markdown2.markdown(post.body, extras=['fenced-code-blocks'])
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 这里覆写的目的是除了将post传递给模板外（PostDetailView已经帮我们实现了）
        # 还要把评论表单form、评论列表comment_list传递给模板detail.html
        context = super(DetailView, self).get_context_data(**kwargs)
        form = CommentForm
        comment_list = self.object.comment_set.all()

        context.update({'form': form,
                        'comment_list': comment_list})
        return context



class TagView(IndexView):
    '''按标签归类文章列表'''
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get("q")
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', context={'error_msg': error_msg})
    else:
        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return render(request, 'blog/index.html', context={'error_msg': error_msg,
                                                           'post_list': post_list})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def blog(request):
    post_list = Post.objects.all()
    return render(request, 'blog/full-width.html', context={'post_list': post_list})

