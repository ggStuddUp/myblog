
from django.conf.urls import url
from . import views


app_name = 'comments'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^comment/post/(?P<post_pk>\d+)/(?P<user_name>.*?)/$', views.post_comment, name='post_comment')
]
