from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status,generics,mixins, viewsets
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from .permissions import *



# Model Viewset
class PostModelViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    
# Viewset
class PostViewset(viewsets.ViewSet):
    def list(self, request:Request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request:Request,pk=None):
        post=get_object_or_404(Post,pk=pk)
        serializer = PostSerializer(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    

# Generic APIView and mixins 
# @permission_classes([])
class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [ReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def get(self,request:Request, *args, **kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



# class PostRetriveUpdateDeleteView(generics.GenericAPIView, mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     permission_classes = [AutherOrReadOnly]
#     def get(self,request:Request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self,request:Request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self,request:Request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class PostListCreateView(APIView):
    """
        a view for creating and listing posts
    """

    serializer_class = PostSerializer
    permission_classes = [ReadOnly]
    def get(self,request:Request,*args,**kwargs):
        posts = Post.objects.all()
        
        serializer = self.serializer_class(instance=posts,many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request:Request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Post created",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostRetriveUpdateDeleteView(APIView):
#     serializer_class = PostSerializer

#     def get(self,request:Request, post_id:int):
#         post = get_object_or_404(Post,pk=post_id)

#         serializer = self.serializer_class(instance=post)

#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def put(self,request:Request,post_id:int):
#         post = get_object_or_404(Post, pk=post_id)

#         data = request.data

#         serializer = self.serializer_class(data=data, instance=post)

#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message":"Updated Successfully",
#                 "data":serializer.data,
#             }

#             return Response(data=response, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request:Request, post_id:int):
#         post = get_object_or_404(Post,pk=post_id)

#         post.delete()

#         return Response(data={"message": "Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)