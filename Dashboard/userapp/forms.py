from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as DjangoUserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError  # Import ValidationError
from .models import CustomUser, Student, Teacher


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = CustomUser
        fields = DjangoUserCreationForm.Meta.fields + (
            'user_type', 'phone', 'address', 'date_of_birth', 'contact_number', 'linkedin_url', 'telegram_url',
            'instagram_url', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the registration form fields (e.g., add CSS classes)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        # Example: Allow usernames shorter than Django's default
        if len(username) < 3:  # Change 3 to your minimum length
            raise ValidationError("Username must be at least 3 characters long.")
        # Add any other custom username validation here

        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("The two password fields didn't match.")

        # Example:  Allow shorter passwords than Django's default
        if len(password) < 6:  # Change 6 to your minimum length
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password2  # Return the cleaned value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']  # Assuming user_type is a field in your form
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone', 'address', 'date_of_birth',
                  'contact_number', 'linkedin_url', 'telegram_url', 'instagram_url', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the profile form fields (e.g., add CSS classes)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_password(self):  # Override password change validation
        password = self.cleaned_data.get('password')

        # Example:  Allow shorter passwords than Django's default
        if password and len(password) < 6:  # Change 6 to your minimum length
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password  # Return the cleaned value

    def save(self, commit=True):
        user = super().save(commit=False)
        # Check if the password was changed and hash it
        if self.cleaned_data.get('password'):
            user.password = make_password(self.cleaned_data['password'])  # Hash the new password
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student', 'group', 'enrollment_date', 'father_fullname', 'father_phone_number', 'mother_fullname',
                  'mother_phone_number']

        widgets = {  # Adding CSS classes for consistent styling
            'student': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'father_fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher', 'recruitment_date']

        widgets = {  # Adding CSS classes for consistent styling
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'recruitment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }