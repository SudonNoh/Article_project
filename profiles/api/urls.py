from django.urls import path, include

from .views import ProfileFollowAPIView, ProfileRetrieveAPIView

urlpatterns = [
    path('<str:username>', ProfileRetrieveAPIView.as_view()),
    path('<str:username>/follow', ProfileFollowAPIView.as_view())
]