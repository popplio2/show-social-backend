from django.shortcuts import render
# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.models import *


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
    # user_serializer = UserSerializer(users, many=True)  # Serialize the users
    return Response(users)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_one_user(request):
    # Get the username from the query parameter
    username = request.GET.get('username', '')

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    user_posts = user.user_post.all().filter(toCommunity=True)

    posts_data = [
        {
            "id": post.id,
            "author": username,
            "title": post.title,
            "show": post.show,
            "text": post.text,
            "added_at": post.added_at,
            # Include other relevant attributes
        }
        for post in user_posts
    ]

    user_data = {
        "id": user.id,
        "username": user.username,
        "posts": posts_data
    }

    return Response(user_data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_show(request):
    show_id = request.data.get('id', '')
    show_name = request.data.get('name', '')
    show_image = request.data.get('image', '')

    existing_show = Show.objects.filter(id=show_id).first()

    if existing_show:
        UserShow.objects.create(user=request.user, show=existing_show)
        added_at = UserShow.objects.filter(
            user=request.user, show=existing_show).first().added_at
        return Response({"added_at": added_at})
    else:
        new_show = Show.objects.create(
            id=show_id, name=show_name, image=show_image)
        UserShow.objects.create(user=request.user, show=new_show)
        added_at = UserShow.objects.filter(
            user=request.user, show=new_show).first().added_at
        return Response({"added_at": added_at})

# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def accept_friend_request(request, request_id):
#     friend_request = FriendRequest.objects.get(id=request_id)
#     if friend_request.receiver == request.user.userprofile and friend_request.status == 'pending':
#         friend_request.status = 'accepted'
#         friend_request.save()
#         Friend.objects.create(user=friend_request.sender,
#                               friend=friend_request.receiver)
#         Friend.objects.create(user=friend_request.receiver,
#                               friend=friend_request.sender)
#         return Response({'detail': 'Friend request accepted.'})
#     else:
#         return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
