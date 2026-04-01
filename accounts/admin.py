from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # ro'yxatda ko'rinadigan ustunlar
    list_display = ("username", "role", "position", "phone", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "phone", "position")
    list_filter = ("role", "is_staff", "is_active")

    # User edit sahifasida ko'rinadigan bo'limlar
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Shaxsiy ma'lumot", {"fields": ("first_name", "last_name", "email")}),
        ("Xodim ma'lumotlari", {"fields": ("role", "position", "phone", "photo")}),  # ✅ shu yerda chiqadi
        ("Ruxsatlar", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Muhim vaqtlar", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "role", "position", "phone", "photo"),
        }),
    )
