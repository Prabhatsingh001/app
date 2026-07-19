"""Admin configuration for the StudyBuddy user models."""

from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Customize the admin list view for custom users."""

    list_display = ["id", "email", "username", "phone_number"]
    list_display_links = ["id", "email", "username"]
