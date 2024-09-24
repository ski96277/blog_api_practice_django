from . import views
from django.urls import path

urlpatterns = [

    path('',views.PostListCreationView.as_view(),name='Get All post api'),
    path('update_delete_retrieve/<int:pk>',views.PostRetrieveUpdateDeleteView.as_view(),name="Posts_Create api"),
    
    
]