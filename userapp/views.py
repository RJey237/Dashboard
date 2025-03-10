# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from .models import CustomUser, Groups, Student,Teacher,TeacherGroup
from .forms import LoginForm, UserCreationForm,UsernameOrEmailPasswordResetForm
from django.contrib.auth import get_user_model  

User = get_user_model() 

def login_view(request):
    print("Log_in view accessed")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST) 
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  

            if user is not None: 
                login(request, user)
                print(f"User '{user.username}' logged in successfully")
                messages.success(request, "Logged in successfully!") 
                return redirect('group_list') 

            else:
                print("Authentication Failed!")
                messages.error(request, "Invalid username or password.") 
                return render(request, 'new/ventic/Login.html', {'form': form})

        else:
            print("Form is invalid")
            print(form.errors) 

            return render(request, 'new/ventic/Login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'new/ventic/Login.html', {'form': form})
    
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


def password_reset_request(request):
    if request.method == "POST":
        form = UsernameOrEmailPasswordResetForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.error(request, "Invalid username. Try again")
                    return render(request=request, template_name="registration/password_reset_form.html", context={"form": form}) 

            else:  
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    messages.error(request, "Invalid email. Try again")
                    return render(request=request, template_name="registration/password_reset_form.html", context={"form": form})

            subject = "Password reset requested"
            message = "Reset your password by clicking the following link"
            from_email = 'admin@example.com'
            html_message = render_to_string('emails/password_reset_email.html', {
                    'reset_url': "https://yourdomain.com/resetpassword",
            })
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

            messages.success(request, 'Password reset email sent successfully')
            return redirect("password_reset_done")  

        else:
            messages.error(request, 'Invalid data, correct and try again')

    else:
        form = UsernameOrEmailPasswordResetForm()  

    return render(request=request, template_name="registration/password_reset_form.html", context={"form": form})




@login_required
def group_list(request):
    user = request.user  # 
    if is_admin(user):
        groups = Groups.objects.all()
        users = CustomUser.objects.all()  
        teachers = CustomUser.objects.filter(user_type=CustomUser.UserTypeEnum.TEACHER)
    elif is_teacher(user):
        teacher_profile = get_object_or_404(Teacher, teacher=user)
        groups = Groups.objects.filter(teachergroup__teacher=teacher_profile) 
        users, teachers = None, None
    elif is_student(user):
        student = get_object_or_404(Student, student=user) 
        groups = [student.group] if student.group else []  
        users, teachers = None, None  # 
    else:
        messages.warning(request, "You do not have permission to view this page.")
        return redirect('login')

    return render(request, 'new/ventic/index.html', {
        'groups': groups,
        'users': users,
        'teachers': teachers,
        'user_type': user.user_type,
    })


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

def calendar(request):
    return render(request, 'new/ventic/calendar.html')
def clients_grid(request):
    return render(request, 'new/ventic/clients-grid.html')
def profile(request):
    return render(request, 'new/ventic/Profile.html')
