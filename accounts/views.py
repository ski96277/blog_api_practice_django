from django.shortcuts import render
from .serializers import SignupSerializer
from rest_framework import generics, status
from rest_framework.request import Request
from django.http import JsonResponse


# Create your views here
class SignupView(
    generics.GenericAPIView,
):
    serializer_class = SignupSerializer

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(
            data=serializer.errors,
            status=status.HTTP_404_NOT_FOUND,
        )
