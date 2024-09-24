from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from rest_framework.decorators import api_view,APIView
from .serializers import PostSerializer
from .models import Post
from rest_framework import status
from rest_framework.request import Request

#Create Class based generic and mixin class

class PostListCreationView(APIView):
    """
    A view for creating and listing posts
    """
    serializer_class = PostSerializer
    def get(self,request:Request, *args, **kwargs):
        posts = Post.objects.all();
        serializer = self.serializer_class(instance = posts,many = True)
        return JsonResponse(data={"posts":serializer.data},status = status.HTTP_200_OK)
    
    def post(self,request:Request,*args, **kwargs):
        data  = request.data
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message":"Data Saved","post":serializer.data},status = status.HTTP_201_CREATED)
        return JsonResponse({"message":"Data invalid"},status = status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateDeleteView(APIView):

    serializer_class = PostSerializer

    def get(self,request:Request,post_id:int):
        try:
            post = Post.objects.get(pk = post_id)
        except Post.DoesNotExist:
            return JsonResponse(data={"message":"post id is not found"})
        
        serializer = self.serializer_class(post)
        return JsonResponse(data= {"message":"Post Data","post":serializer.data})
    
    def put(self,request:Request,post_id:int):

        try:
            post = Post.objects.get(pk = post_id)
        except Post.DoesNotExist:
            return JsonResponse(data={"message":"post id is not found"})
        
        serializer = PostSerializer(post,request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data={"message":"Post data update",'post':serializer.data})
        return  JsonResponse(data={"message":"post Data is not valid"})

    def delete(self,request: Request,post_id:int):
        try:
                
            post = Post.objects.get(pk = post_id)
            post.delete()
            return JsonResponse(data={"message":"post data deleted"})
        except Post.DoesNotExist:
            return JsonResponse(data={"message":"post data Not found"})
