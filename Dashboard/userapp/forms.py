from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as DjangoUserCreationForm
from .models import CustomUser, Student, Teacher


class LoginForm(AuthenticationForm):  # Authentication form
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserCreationForm(DjangoUserCreationForm):  # Creation form, can add custom attributes
    class Meta(DjangoUserCreationForm.Meta):
        model = CustomUser
        fields = DjangoUserCreationForm.Meta.fields + (
            'user_type', 'phone', 'address', 'date_of_birth', 'contact_number', 'linkedin_url', 'telegram_url',
            'instagram_url')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student', 'group', 'enrollment_date', 'father_fullname', 'father_phone_number', 'mother_fullname',
                  'mother_phone_number']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher', 'recruitment_date']