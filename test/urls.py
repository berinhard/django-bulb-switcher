# coding:utf-8
from django.conf.urls import patterns, url
from django.http import HttpResponse

def view(request):
    return HttpResponse('ok')

urlpatterns = patterns('',
    url(r'^/$', view),
)
