from . import views
from django.urls import path

urlpatterns = [

    path('',views.getAllPost,name='Get All post api'),
    path('create/',views.postCreate,name="Posts_Create api"),
    path('update/<int:post_id>',views.postUpdate,name='Post update api'),
    path('delete/<int:post_id>',views.postDelete,name = 'Post Deleted Api')
]