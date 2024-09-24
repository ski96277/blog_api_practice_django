from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from .models import Post
from rest_framework import status

#Create Class based generic and mixin class



# Create your Function Based views here.
@api_view(['POST'])
def postCreate(request: HttpRequest):
    if request.method == "POST":
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'post':serializer.data},status = status.HTTP_201_CREATED)
    
        return JsonResponse({"message":"Data is invalid"},status  = status.status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getAllPost(request):

    if request.method =="GET":

        postModel = Post.objects.all()
        serializer = PostSerializer(postModel,many = True)
        
        return JsonResponse({"posts":serializer.data},status = status.HTTP_200_OK)
    
@api_view(['PUT'])
def postUpdate(request:HttpRequest, post_id:int):
    if request.method == 'PUT':
        try:
            postModel = Post.objects.get(pk = post_id)
        except Post.DoesNotExist:
            return JsonResponse({"message":"Post not found"},status = status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(postModel,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message":"Post updated","post":serializer.data},status = status.HTTP_200_OK)
        return JsonResponse({"message":"Post data is not valid"},status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def postDelete(request:HttpRequest, post_id:int):
    if request.method == "DELETE":
        try:
            postModel = Post.objects.get(pk = post_id)
            postModel.delete()
            return JsonResponse({"message":"post data deleted"},status = status.HTTP_200_OK)
        except Post.DoesNotExist:
            return JsonResponse({"message":"Post data not found"},status = status.HTTP_404_NOT_FOUND)