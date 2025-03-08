# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  
from .models import CustomUser, Groups, Student  
from .forms import LoginForm, UserCreationForm 
from django.db.models import Q
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  # Import the LoginForm


def login_view(request):
    print("Log_in view accessed")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password')) # Use username and password from cleaned_data
            if user:
                login(request, user)
                print(f"User '{user.username}' logged in successfully")
                messages.success(request, f"User '{user.username}' logged in successfully")
                return redirect('group_list')  # Corrected the URL name
            else:
                print("Authentication Failed!")
                messages.error(request, "Authentication failed")
                return render(request, 'login.html', {'form': form})
        else:
            print("Form is invalid")
            print(form.errors) #print form errors here.
            messages.error(request, "Form is invalid")
            return render(request, 'login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "Successfully logged out.")  
    return redirect('login') 


def is_admin(user):
    return user.user_type == 'admin'


def is_teacher(user):
    return user.user_type == 'teacher'


def is_student(user):
    return user.user_type == 'student'



@login_required
def group_list(request):
    """Displays a list of groups. Admins see all, teachers see only their groups."""
    if is_admin(request.user):
        groups = Groups.objects.all() 
    elif is_teacher(request.user):
         groups = Groups.objects.all()
    else:
        messages.warning(request, "You do not have permission to view groups.")
        return redirect('login') 
    return render(request, 'group_list.html', {'groups': groups})



@login_required
def group_detail(request, group_id):
    """Displays a group's details, students, teacher (if applicable), and attendance form."""
    group = get_object_or_404(Groups, pk=group_id)

    if is_admin(request.user) or is_teacher(request.user):
        students = Student.objects.filter(group=group)
        teacher = request.user if is_teacher(request.user) else None 


        return render(request, 'group_detail.html', {'group': group, 'students': students, 'teacher': teacher})
    else:
        messages.warning(request, "You do not have permission to view this group's details.")
        return redirect('home')



@login_required
def student_info(request):
    """Displays a student's information and lessons."""
    if is_student(request.user):
        student = get_object_or_404(Student, pk=request.user.pk)  
        group = student.group



        return render(request, 'student_info.html', {'student': student, 'group': group})

    else:
        messages.warning(request, "You do not have permission to view student information.")
        return redirect('home')

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'admin_panel.html')

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Displays a list of all users (admins, teachers, students)."""
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    """Creates a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
        else:
            messages.error(request, 'User creation failed.')
    else:
        form = UserCreationForm()
    return render(request, 'user_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    """Updates an existing user."""
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
        else:
            messages.error(request, 'User update failed.')
    else:
        form = UserCreationForm(instance=user)
    return render(request, 'user_update.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """Deletes an existing user."""
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'user_delete.html', {'user': user})

@login_required
@require_POST
def toggle_user_active(request, pk):
    """Toggles the is_active status of a user."""
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {user.username} {'activated' if user.is_active else 'deactivated'} successfully.")
    return redirect('user_list')