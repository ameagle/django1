from django.urls import path
from .views import *
urlpatterns = [
    path('',                  posts_list,name='posts_list_url'),
    path('post/<str:slug>/', posts_detail ,name='post_detail_url'),
    #path('blog/', include()),
]