from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as DjangoUserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError  
from .models import CustomUser, Student, Teacher


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].required = True  
        self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist.") 
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = self.user_cache  

            if user is None:
                raise forms.ValidationError("Invalid username or password.")




class UsernameOrEmailPasswordResetForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}) 
    )
    email = forms.EmailField(
        label="Email Address",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}) 
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username and not email:
            raise forms.ValidationError("Please enter either a username or an email address.")

        if username and email:
            raise forms.ValidationError("Please enter either a username or an email address, not both.")


        if username:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid username. Try again")

        if email:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email. Try again")


        return cleaned_data

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = CustomUser
        fields = DjangoUserCreationForm.Meta.fields + (
            'user_type', 'phone', 'address', 'date_of_birth', 'contact_number', 'linkedin_url', 'telegram_url',
            'instagram_url', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 3:  
            raise ValidationError("Username must be at least 3 characters long.")


        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("The two password fields didn't match.")

        if len(password) < 6:  
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password2 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type'] 
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
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_password(self):  
        password = self.cleaned_data.get('password')

        if password and len(password) < 6: 
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password  

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password'):
            user.password = make_password(self.cleaned_data['password'])  
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student', 'group', 'enrollment_date', 'father_fullname', 'father_phone_number', 'mother_fullname',
                  'mother_phone_number']

        widgets = {  
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

        widgets = {  
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'recruitment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }