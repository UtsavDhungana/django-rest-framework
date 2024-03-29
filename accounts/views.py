from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from .tokens import *

@permission_classes([])
class SignUpView(generics.GenericAPIView,):
    serializer_class = SignUpSerializer

    def post(self, request:Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User Created Successfully",
                "data": serializer.data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([]) 
class LoginView(APIView):

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        
        serializer = SignUpSerializer(instance=user)
        if user is not None:
            tokens = create_jwt_pair_for_user(user=user)
            response = {
                "message": "Login Successful",
                "user": serializer.data,
                "token": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request:Request):
        content = {
            "user": str(request.user),
            "auth":str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)