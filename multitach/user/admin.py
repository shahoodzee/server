from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser,Worker,Client
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('email', 'is_staff', 'is_active', 'image_url', 'date_of_birth', 'gender', 'phone')
    list_filter = ('email','is_staff','is_active',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('image_url', 'date_of_birth', 'gender', 'phone')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Worker)
admin.site.register(Client)

    
    