from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Post, Preference


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'enrichment', 'email_deliverability',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}),)
    list_display = ['email', 'username', 'email_deliverability', ]


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('likes', )


class PreferenceAdmin(admin.ModelAdmin):
    readonly_fields = ('like', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Preference, PreferenceAdmin)
