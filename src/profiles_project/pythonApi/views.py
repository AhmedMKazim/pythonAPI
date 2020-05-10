from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework import status
from . import serializers

# Create your views here.
class HellowApiView(APIView):
    """Test API View."""

    serializer_class = serializers.HelloSerializer; # describe the serializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""
        an_apiview = [
            'Uses HTTP methods as functin (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message': 'Hellow!', 'an_apiview': an_apiview})

    def post(self, request):
        """ Create a hellow message with our nme."""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handles updating an object."""

        return Response({'method': 'put'})
    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""
        return Response({'method': 'patch'})
    def delete(self, request, pk=None):
        """Deletes and object."""
        return Response({'method': 'delete'})
class HelloViewSet(viewsets.ViewSet):
    def list(self, request):
        """Return a hello message."""
        an_viewset = [
            'Uses HTTP methods as functin (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_viewset': an_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'messge': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""
        return Response({'http_method': 'GET'})
    def update(self, request, pk=None):
        """Handles updating an object."""
        return Response({'http_method': 'PUT'})
    def partial_update(self, request, pk= None):
        """Handles updating part of an object."""
        return Response({'http_method': 'PATCH'})
    def destroy(self, request, pk=None):
        """Handles removing an object."""
        return Response({'http_method': 'DELETE'})
