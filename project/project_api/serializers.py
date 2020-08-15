from rest_framework import serializers
from . import models

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.UserProfile
    fields = ('id', 'email', 'name', 'phone', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    """Create and return a new user."""

    user = models.UserProfile(
      email=validated_data['email'], 
      name=validated_data['name'],
      phone=validated_data['phone'],
    )

    user.set_password(validated_data['password'])
    user.save()

    return user

class ServiceCategoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.ServiceCategories
    fields = ('id', 'name')

  def create(self, validated_data):
    service_category = models.ServiceCategories(name=validated_data['name'])

    service_category.save()
    return service_category


class ServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Service
    fields = ('id', 'name', 'providerName', 'providerFirstName', 'cat', 'short_description', 'rating', 'created_at', 'lat', 'lon')
  # def create(self, validated_data):
  #   service = models.Service(
  #     name=validated_data['name'],
  #     provider_name=validated_data['provider_name'],
  #     provider_firstname=validated_data['provider_firstname'],
  #     cat=validated_data['cat'],
  #     short_description=validated_data['short_description'],
  #     rating=validated_data['rating']
  #     lat
  #   )

class ServiceListSerializer(serializers.Serializer):
  list = serializers.ListField(child=ServiceSerializer())
    
    