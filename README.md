
# Blog Api With various type of Views

I'm creating a project where i will add diffrent types of view like class Based and Function Based and Generic API Views And Model Mixins

## Function Based CURD Api


#### Views.py

```javascript
from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from .models import Post
from rest_framework import status

# Function Based views here.
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

```



#### urls.py

```javascript

from . import views
from django.urls import path

urlpatterns = [

    path('',views.getAllPost,name='Get All post api'),
    path('create/',views.postCreate,name="Posts_Create api"),
    path('update/<int:post_id>',views.postUpdate,name='Post update api'),
    path('delete/<int:post_id>',views.postDelete,name = 'Post Deleted Api')
]

```

## models.py

``` javascript
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    createdAt= models.DateTimeField(auto_now_add= True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    


```


## Class Based CRUD Api


#### Views.py

```javascript

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


```



#### urls.py

```javascript

from . import views
from django.urls import path

urlpatterns = [

    path('',views.PostListCreationView.as_view(),name='Get All post api'),
    path('update_delete_retrieve/<int:post_id>',views.PostRetrieveUpdateDeleteView.as_view(),name="Posts_Create api"),
    
]

```


## Mixins and generics Based CURD Operation


#### Views.py

```javascript


from .serializers import PostSerializer
from .models import Post
from rest_framework import generics,mixins
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


```

#### Views.py

```javascript

from . import views
from django.urls import path

urlpatterns = [

    path('',views.PostListCreationView.as_view(),name='Get All post api'),
    path('update_delete_retrieve/<int:pk>',views.PostRetrieveUpdateDeleteView.as_view(),name="Posts_Create api"),
    
    
]

```


