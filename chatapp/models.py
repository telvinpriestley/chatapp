from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL , null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    # participants = models.IntegerField()
    shares = models.IntegerField(default=0)
    banstatus = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class RoomLike(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomlike_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.room.name}"
    
class RoomComment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomcomment_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.room.name}"

class CommentLike(models.Model):
    comment = models.ForeignKey(RoomComment, on_delete=models.CASCADE, related_name='commentlike_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.comment.user.username}'s comment on {self.comment.room.name}"

class CommentReply(models.Model):
    comment = models.ForeignKey(RoomComment, on_delete=models.CASCADE, related_name='commentreply_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} replied to {self.comment.user.username}'s comment on {self.comment.room.name}"
    
class RoomShare(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomshare_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} shared {self.room.name}"
 

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='details')
    job = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False)
    contact = models.IntegerField()
    address = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(
        max_length=6,
        choices=[("Male", "Male"), ("Female", "Female")],
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f"Details of {self.user.username} "
 
    
class Tempstore(models.Model):
    fname = models.CharField(max_length=200, blank=True, null=True)
    lname = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)