from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import *
from django.views.generic import View
from .utils import ObjectDetailMixin,ObjectCreateMixin
from .forms import TagForm, PostForm
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.response import Response

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
    print("queryset.str:--------------"+str(queryset.query))
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'slug']



#class TagPostRawSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Tag
#        fields = ['id', 'title', 'type']


class TagPostVirtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPostVirtual
        fields = "__all__"


class TagPostRawSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    type = serializers.CharField(max_length=50)
    def create(self, validated_data):
         """
         Create and return a new `Snippet` instance, given the validated data.
         """
         return

    def update(self, instance, validated_data):

        return


class TagSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    slug = serializers.SlugField(max_length=150)
    def create(self, validated_data):
         """
         Create and return a new `Snippet` instance, given the validated data.
         """
         return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        print (validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer2
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def tags_custom_list(request):
    """
    List all code posts
    """


    if request.method == 'GET':
        tags = Tag.objects.filter(id__gt=5)
        serializer = TagSerializer2(tags, many=True)
        return Response(serializer.data)


class TagPostVirtualRawQueryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    sql = """SELECT bp.id as id, bp.title as title, 'type_post' as type FROM blog_post as bp WHERE bp.id >%s
              UNION SELECT bt.id as id, bt.title as title, 'type_tag' as type FROM blog_tag as bt WHERE bt.id >%s""";

    print(sql)
    queryset =  TagPostVirtual.objects.raw(sql,["1","5"])
    #serializer_class = TagPostRawSerializer2 #not wokk paginations for Tag
    serializer_class = TagPostVirtualSerializer  # not catch any field
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        print ("retrieve:",request)
        return super().retrieve(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print("req_list_GET:" , request.GET)
        #print("req_list_META:" , request.META)
        print("req_list_AUTH:", request.auth)
        return super().list(self, request, *args, **kwargs)



