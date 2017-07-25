from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    fields = ['organization_name', 'stripe_id', 'user']
    list_display = ('user', 'organization_name')

admin.site.register(Profile, ProfileAdmin)