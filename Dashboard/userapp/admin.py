from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm, UserChangeForm  # Import custom forms
from .models import CustomUser, Groups, Student, Teacher, DayOfWeek


class CustomUserAdmin(UserAdmin):
    # add_form = UserCreationForm  # Use the custom creation form
    # form = UserChangeForm  # Use the custom change form
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'phone', 'address', 'date_of_birth', 'contact_number',
                    'linkedin_url', 'telegram_url', 'instagram_url', 'image')

    # Redefine the fieldsets to include only your custom fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('user_type', 'phone', 'address', 'date_of_birth', 'contact_number',
                                       'linkedin_url', 'telegram_url', 'instagram_url', 'image')}),
    )

    # Redefine the add_fieldsets to include only the necessary fields for user creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2', 'user_type', 'phone', 'address',
                       'date_of_birth', 'contact_number', 'linkedin_url', 'telegram_url', 'instagram_url',
                       'image')}
         ),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


# Register the models (using the custom UserAdmin for CustomUser)

from django.contrib.auth.hashers import make_password

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    
    def save_model(self, request, obj, form, change):
        # Hash the password only if it's being set manually
        if form.cleaned_data.get('password') and not obj.password.startswith('pbkdf2_sha256$'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(DayOfWeek)
admin.site.register(Groups)
admin.site.register(Student)
admin.site.register(Teacher)      