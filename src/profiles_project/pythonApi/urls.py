from django.urls import path
from . import views


urlpatterns = [
    path('hello-view/', views.HellowApiView.as_view())
]
