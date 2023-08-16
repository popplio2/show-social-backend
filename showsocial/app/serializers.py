from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import *


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'name', 'image']


class UserShowSerializer(serializers.ModelSerializer):
    show = ShowSerializer()  # Use the ShowSerializer to serialize the related Show model

    class Meta:
        model = UserShow
        fields = ['show', 'added_at']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    user_shows = UserShowSerializer(many=True, read_only=True)
    user_posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'testProperty', 'user_shows', 'user_posts')
