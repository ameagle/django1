from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
#router.register(r'', GroupViewSet)

urlpatterns = [

    path('api/', include(router.urls)),
    path('',                posts_list,     name='posts_list_url'),
    path('post/create/',     PostCreate.as_view(),name='post_create_url'), #post_create_url --alias for full path /blog/post/create/
    path('post/<str:slug>/',PostDetail.as_view(),   name='post_detail_url'),
    path('tags/',           tags_list,      name='tags_list_url'),
    path('tag/create/',     TagCreate.as_view(),      name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(),     name='tag_detail_url'),

    path('api/posts/', TagDetail.as_view(),     name='tag_detail_url'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #path('blog/', include()),
]