# api/views.py
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer
from .serializers import UserSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'].lower(), password=serializer.validated_data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = UserSerializer(user).data
            response_data.update({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            return Response(response_data)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.pagination import PageNumberPagination

class UserSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            if '@' in query:
                users = User.objects.filter(email__iexact=query)
            else:
                users = User.objects.filter(name__icontains=query)
        else:
            users = User.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    

    # api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import FriendRequest
from .serializers import FriendRequestSerializer, FriendRequestActionSerializer


class FriendRequestReceivedToMe(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        status_filter = request.query_params.get('status')
        to_user = request.user

        friend_requests = FriendRequest.objects.filter(to_user=to_user, status='pending')
        
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class FriendRequestViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = request.user

        friend_requests = FriendRequest.objects.filter(
             Q(from_user=current_user, status='accepted') | Q(to_user=current_user, status='accepted'))  
        print(friend_requests)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):       
        to_user_id = request.data.get('to_user')
        from_user = request.user

        if not to_user_id:
            return Response({"detail": "Status and to_user are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if  len(FriendRequest.objects.filter(~Q(status='rejected'))
                .filter(from_user=to_user,to_user=from_user ))  != 0:
            return Response({"detail": "User already in friend list or request is pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        if  from_user == to_user:
            return Response({"detail": "You can`t sent friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()

        if recent_requests_count >= 3:
            return Response({"detail": "You have sent too many friend requests in a short period. Please wait before sending more."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        data = {
            'from_user': from_user.id,
            'to_user': to_user.id,
            'status': 'pending'
        }
        
        serializer = FriendRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FriendRequestActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
 
        friend_request = FriendRequest.objects.get(pk=pk)
        from_user = request.user
        if friend_request.to_user == from_user:
            serializer = FriendRequestActionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            action = serializer.validated_data['action']
            if action == 'accept':
                friend_request.status = 'accepted'
            elif action == 'reject':
                friend_request.status = 'rejected'
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data)
        else:
            return Response({"detail": "You are not authorize to perform this action"}, status=status.HTTP_400_BAD_REQUEST)


