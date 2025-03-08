# urls.py
from django.urls import path
from .views import login_view,logout_view,group_list,group_detail,student_info,admin_panel,user_list,user_create,user_update,user_delete,toggle_user_active

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('groups/', group_list, name='group_list'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('student/info/', student_info, name='student_info'),


    path('admin_panel/', admin_panel, name='admin_panel'),
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:pk>/update/', user_update, name='user_update'),
    path('users/<int:pk>/delete/', user_delete, name='user_delete'),
    path('users/<int:pk>/toggle_active/', toggle_user_active, name='toggle_user_active'),  
]