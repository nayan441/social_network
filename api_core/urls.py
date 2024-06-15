from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestActionView, FriendRequestViewSet, FriendRequestReceivedToMe
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-requests/', FriendRequestViewSet.as_view(), name='friend-request'),
    path('friend-requests-received/', FriendRequestReceivedToMe.as_view(), name='friend-request-received'),
    path('friend-requests/<int:pk>/action/', FriendRequestActionView.as_view(), name='friend-request-action'),
]


