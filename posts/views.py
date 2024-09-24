from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from rest_framework.decorators import api_view,APIView
from .serializers import PostSerializer
from .models import Post
from rest_framework import status,generics,mixins
from rest_framework.request import Request

#Create Class based generic and mixin class

class PostListCreationView(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    """
    A view for creating and listing posts
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    def get(self,request:Request, *args, **kwargs):

        return self.list(request=request,*args,**kwargs)      

    def post(self,request:Request,*args, **kwargs):
        
        return self.create(request=request,*args,**kwargs)
        
class PostRetrieveUpdateDeleteView(generics.GenericAPIView,mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,mixins.RetrieveModelMixin):

    serializer_class = PostSerializer
    queryset = Post.objects.all()    

    def get(self,request:Request,*args,**kwargs):
        return self.retrieve(request=request,*args,**kwargs)
    def put(self,request:Request,*args, **kwargs):

       return self.update(request= request, *args, **kwargs)
    

    def delete(self,request: Request,*args, **kwargs):
        return self.destroy(request= request,*args, **kwargs)
