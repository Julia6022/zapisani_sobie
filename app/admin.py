from django.contrib import admin
from .models import UserProfile, Message, User

admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(User)