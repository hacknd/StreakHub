from django.contrib import admin

# Register your models here.
from client_audit.models import Limit, UserActions

admin.site.register(Limit)
admin.site.register(UserActions)
