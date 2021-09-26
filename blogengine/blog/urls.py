from django.urls import path,include
from .views import *
from rest_framework import routers

from rest_framework.schemas import get_schema_view # new

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet) # blog/api/posts/
router.register(r'tags', TagViewSet)    # blog/api/tags/
router.register(r'raw', TagPostVirtualRawQueryViewSet)    # blog/api/raw/
#router.register(r'ctags', tags_custom_list)    # blog/api/ctags/


schema_view = get_schema_view(title='Blog API') # new


urlpatterns = [
    #http://mw.ixi.ru:8001/users/2/?format=json
    path('',                posts_list,     name='posts_list_url'),
    path('api/', include(router.urls)),
    path('api/ctags/',tags_custom_list,name='tags_custom_list'), #blog/api/ctags/
    path('raw/',TagPostVirtualRawQueryView.as_view(),name='tags_raw'), #blog/raw/

    path('post/create/',     PostCreate.as_view(),name='post_create_url'), #post_create_url --alias for full path /blog/post/create/
    path('post/<str:slug>/',PostDetail.as_view(),   name='post_detail_url'),
    path('tags/',           tags_list,      name='tags_list_url'),
    path('tag/create/',     TagCreate.as_view(),      name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(),     name='tag_detail_url'),

    path('api/rest-auth/', include('rest_auth.urls')), # api/rest-auth/login

    path('schema/', schema_view),  # new

    #path('api/posts/', TagDetail.as_view(),     name='tag_detail_url'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #path('blog/', include()),
]