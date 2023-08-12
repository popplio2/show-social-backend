from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.


class UserProfile(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    # email, profilePic, myShows, posts, friends

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), (
        'rejected', 'Rejected')], default='pending', max_length=10)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class Friend(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='friends')

    def __str__(self):
        return f"{self.user.user.username} & {self.friend.user.username}"


class UserShow(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    show = models.ForeignKey('Show', on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.show.title}"


class Show(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    image = models.URLField()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name='user_posts')
    title = models.TextField(blank=False)
    show = models.ForeignKey(
        'Show', on_delete=models.SET_NULL, null=True, related_name='show_posts')
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    toCommunity = models.BooleanField()
    toFriends = models.BooleanField()

    def __str__(self):
        return self.name
