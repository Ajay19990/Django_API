from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import permissions
from . import models

class UserProfileViewSet(viewsets.ModelViewSet):
  """Handles creating, reading and updating profiles."""

  def create(self, req):
    serializer = serializers.UserProfileSerializer(data=req.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

  serializer_class = serializers.UserProfileSerializer
  queryset = models.UserProfile.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (permissions.UpdateOwnProfile,)

  def list(self, req):
    return Response({'error':'only post req allowed'})


class LoginViewSet(viewsets.ViewSet):
  """Checks email and password and returns an auth token."""

  serializer_class = AuthTokenSerializer

  def create(self, req):
    return ObtainAuthToken().post(req)