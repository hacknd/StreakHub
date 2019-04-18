from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Member)
admin.site.register(Community)
admin.site.register(Tournament)
admin.site.register(Bookmarks)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Followers)

