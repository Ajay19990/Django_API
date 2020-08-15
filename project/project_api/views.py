from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import random

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

  serailizer_class = AuthTokenSerializer

  def create(self, req):
    """Use the ObtainAuthToken APIView to validate and create a token."""

    return ObtainAuthToken().post(req)
  # """Checks email and password and returns an auth token."""

  # serializer_class = AuthTokenSerializer

  # def create(self, req):
  #   print('user matches1')
    
  #   username = req.data.get('email')
  #   print('user matches3')
  #   user_from_db = models.UserProfile.objects.get(email__iexact=username)
  #   print('user matches4')
  #   phone_from_db = getattr(user_from_db, 'phone')
  #   print('user matches5')
  #   phone_from_req = str(req.data.get('phone'))
  #   print('user matches6')
  #   try:
  #     print('user matches7')
  #     if (phone_from_req == str(phone_from_db)):
  #       print('user matches8')
  #       return ObtainAuthToken().post(req)
  #     # user = models.UserProfile.objects.filter(phone__iexact=phone)
  #     # if user.exists():
  #     #   return ObtainAuthToken().post(req)
  #   except:
  #     return Response({'badreq':False})

class GetServiceList(viewsets.ModelViewSet):
  queryset = models.Service.objects.all()
  serializer_class = serializers.ServiceSerializer
  authentication_classes = (TokenAuthentication,)
  http_method_names = ['get']


class ValidatePhoneSendOTP(APIView):

  def post(self, req):
    phone_number = req.data.get('phone')
    if phone_number:
      phone = str(phone_number)
      user = models.UserProfile.objects.filter(phone__iexact = phone)
      if user.exists():
        return Response({
          'status': False,
          'detail': 'Phone number is already exists.'
        })
      else:
        key = send_otp(phone)
        old = models.PhoneOTP.objects.filter(phone__iexact=phone)
        if old.exists():
          old = old.first()
          count = old.count
          if count > 10:
            return Response({'status': False, 'detail':'Limit reached'})
          old.count = count + 1
          old.save()
          print(old)
          return Response({
            'status': True,
            'detail': 'Otp sent successfully'
          })

        else: 
          models.PhoneOTP.objects.create(phone=phone, otp=key)
          req.get('https://2factor.in/API/V1/27e56fcb-de2b-11ea-9fa5-0200cd936042/SMS/+91{0}/{1}}'.format(phone, key))
          return Response({
            'status': True,
            'detail': 'Otp sent successfully'
          })

    else:
      return Response({
        'status': False,
        'detail': 'Phone number is not given.'
      })

def send_otp(phone):
    if phone:
      key = random.randint(999,9999)
      return key
    else:
      return False

class ValidateOTP(APIView):
  """Handles post req with a phone and otp to confirm the otp."""

  def post (self, req):
    phone = req.data.get('phone', False)
    otp_sent = req.data.get('otp', False)

    if phone and otp_sent:
      old = models.PhoneOTP.objects.filter(phone__iexact=phone)
      if old.exists():
        old = old.first()
        otp = old.otp
        if str(otp_sent) == str(otp):
          old.validated = True
          old.save()
          return Response({
            'status': True,
            'detail': 'OTP matched, please proceed for registration.'
          })

        else:
          return Response({
            'status': False,
            'detail': 'OTP Incorrect.'
          })

      else:
        return Response({
          'status': False,
          'detail': 'First proceed via sending OTP req.'
        })

    else :
      return Response({
        'status': False,
        'detail': 'Please provide both phone and otp for validation.'
      })
