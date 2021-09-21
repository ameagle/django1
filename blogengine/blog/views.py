from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
def posts_list(request):
    #return HttpResponse('<h1>Hello world1</h1>')
    posts = Post.objects.all()
    return render(request,'blog/index.html',context={'posts':posts})

def posts_detail(request,slug):
    slug = slug[:-1]
    post = Post.objects.get(slug__iexact=slug)
    return render(request, 'blog/post_detail.html', context={'post': post})

# Create your views here.
