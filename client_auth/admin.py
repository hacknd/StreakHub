from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

from .forms import *


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = get_user_model()
	list_display = ('username','email','is_staff', 'is_active',)
	list_filter =('email','is_staff', 'is_active',)
	fieldsets = (
		(None, {'fields':('username', 'email', 'password')}),
		('Permissions', {'fields':('is_staff', 'is_active')}),
		)
	add_fieldsets = (
		(None, {
			'classes':('wide',),
			'fields': ('username','email','password1','password2','is_staff','is_active')
			}),
		)
	search_fields = ('username','email',)
	ordering = ('username','email',)

admin.site.register(get_user_model(), CustomUserAdmin)	
admin.site.register(Role)