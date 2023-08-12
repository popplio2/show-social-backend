from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from djoser.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth.models import User
from app.models import UserProfile


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    # Get the search input from the query parameter
    search_input = request.GET.get('search', '')
    current_user = request.user  # Get the authenticated user who sent the request
    users = UserProfile.objects.filter(
        is_superuser=False,  # Exclude admins
        username__icontains=search_input  # Filter by username containing the search input
    ).exclude(id=current_user.id)  # Exclude the current user
    user_serializer = UserSerializer(users, many=True)  # Serialize the users
    return Response(user_serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_one_user(request):
    # Get the search input from the query parameter
    username = request.GET.get('username', '')
    user = request.GET.get(username=username)
    return Response(user.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_one_user(request):
#     # Get the search input from the query parameter
#     username = request.GET.get('username', '')

#     try:
#         user = UserProfile.objects.get(user__username=username)
#         user_data = {
#             'username': user.user.username,
#             'public_shows': user.added_shows.filter(is_public=True).values('id', 'name', 'image'),
#             'public_posts': user.posts.filter(toFriends=False).values('id', 'text', 'added_at')
#         }
#         return Response(user_data)
#     except UserProfile.DoesNotExist:
#         return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
