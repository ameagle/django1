from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post, Tag
from django.views.generic import View
from .utils import ObjectDetailMixin,ObjectCreateMixin
from .forms import TagForm, PostForm
from rest_framework import routers, serializers, viewsets, permissions

def posts_list(request):
    #return HttpResponse('<h1>Hello world1</h1>')
    posts = Post.objects.all()
    return render(request,'blog/index.html',context={'posts':posts})

#def posts_detail(request,slug):
#    slug = slug[:-1] #del last symbol
#    post = Post.objects.get(slug__iexact=slug)
#    return render(request, 'blog/post_detail.html', context={'post': post})

class PostDetail(ObjectDetailMixin,View):
    model = Post
    template = 'blog/post_detail.html'
    #def get(self,request, slug):
    #    slug = slug[:-1]  # del last symbol
    #    post = get_object_or_404(Post,slug__iexact=slug)
    #    #post = Post.objects.get(slug__iexact=slug)
    #    return render(request, 'blog/post_detail.html', context={'post': post})

class PostCreate(ObjectCreateMixin,View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    # def get(self, request):
    #     form = PostForm()
    #     return render(request, 'blog/post_create_form.html', context={'form': form})
    # def post(self,request):
    #     bound_form = PostForm(request.POST)
    #     if bound_form.is_valid():
    #         new_post=bound_form.save()
    #         return redirect(new_post)
    #     return render(request,'blog/post_create_form.html',context={'form':bound_form})
########## Tag ##############
class TagDetail(ObjectDetailMixin,View):
    model = Tag
    template = 'blog/tag_detail.html'
    #def get(self,request,slug):
    #    tag = Tag.objects.get(slug__iexact=slug)
    #    return render(request, 'blog/tag_detail.html', context={'tag': tag})

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

#def tag_detail(request,slug):
#    tag = Tag.objects.get(slug__iexact=slug)
#    return render(request, 'blog/tag_detail.html', context={'tag': tag})

class TagCreate(ObjectCreateMixin,View):
    template = 'blog/tag_create.html'
    model_form = TagForm
    # def get(self,request):
    #     form = TagForm()
    #     return render(request, 'blog/tag_create.html',context={'form':form})
    #
    # def post(self,request):
    #     bound_form = TagForm(request.POST)
    #     if bound_form.is_valid():
    #         new_tag=bound_form.save()
    #         return redirect(new_tag)
    #     return render(request,'blog/tag_create.html',context={'form':bound_form})
    #     #print(request.POST)



##### Api

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'slug','body']

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'slug']

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]