from django.urls import path
from . import views
from django.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile')
router.register('login', views.LoginViewSet, basename='login')
router.register('services-list', views.GetServiceList)
router.register('categories', views.GetCategoryList)

urlpatterns = [
    path('', include(router.urls)),
    path('validate-phone/', views.ValidatePhoneSendOTP.as_view()),
    path('validate-otp/', views.ValidateOTP.as_view()),
    path('service-list-bycategories/<int:catId>', views.get_servicelist_bycategoty, name='service-list-bycategories'),
    path('follow-service/<int:serviceId>', views.follow_service, name='follow-service'),
    path('get_following_services/', views.get_following_services, name='get_following_services')
]
