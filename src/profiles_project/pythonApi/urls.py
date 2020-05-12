from django.urls import path
from . import views

from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router =  DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginVieSet, basename='login')
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HellowApiView.as_view()),
    path('', include(router.urls))
]
