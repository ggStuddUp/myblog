"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.feeds import AllPostRssFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('blog.urls', namespace='blog')),
    url(r'^', include('comments.urls', namespace='comments')),
    url(r'^all/rss$', AllPostRssFeed(), name='rss'),
    url(r'^users/', include('users.urls', namespace='users')),
    # django内置的用户登录、修改密码、找回密码等函数封装在以下urls文件中：
    url(r'^users/', include('django.contrib.auth.urls')),
]

# django.contrib.auth.urls包含的视图函数：
"""
^users/login/$ [name='login']
^users/logout/$ [name='logout']
^users/password_change/$ [name='password_change']
^users/password_change/done/$ [name='password_change_done']
^users/password_reset/$ [name='password_reset']
^users/password_reset/done/$ [name='password_reset_done']
^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^users/reset/done/$ [name='password_reset_complete']
"""
