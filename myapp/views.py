from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializer import BlogSerializer
# Create your views here.

class BlogList(APIView):

    def get(self,request):
        blogs=Blog.objects.all()
        serializer=BlogSerializer(blogs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class BlogDetail(APIView):
     
    def get_object(self,pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def get(self,request,pk):
        blog=self.get_object(pk)
        if not blog:
            return Response({'error':'Blog not found'},status=404)

        serializer=BlogSerializer(blog)
        return Response(serializer.data)
    
    def put(self,request,pk):
        blog=self.get_object(pk)
        if not blog:
            return Response({'error':'Blog not found'},status=404)
        serializer=BlogSerializer(blog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

    
    def patch(self,request,pk):
        blog=self.get_object(pk)
        if not blog:
            return Response({'error':'Blog not found'},status=404)
        
        serializer = BlogSerializer(blog,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        blog=self.get_object(pk)
        if not blog:
            return Response({'error':'Blog not found'},status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response({'message': 'Blog deleted successfully'},status.HTTP_200_OK)










