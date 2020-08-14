from django.urls import path
from . import views
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile')
router.register('login', views.LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]
