from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(RoomShare)
admin.site.register(UserDetails)
admin.site.register(RoomLike)
admin.site.register(RoomComment)
admin.site.register(CommentLike)
admin.site.register(CommentReply)