
from django.conf.urls import url
from blog import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchiveView.as_view(), name='archives'),
    url(r'^category/(?P<pk>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>\d+$)', views.TagView.as_view(), name='tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^blog/$', views.blog, name='blog'),
]
