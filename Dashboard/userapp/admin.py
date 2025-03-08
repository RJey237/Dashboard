from django.contrib import admin
from .models import CustomUser, Groups, Student,Teacher,DayOfWeek
admin.site.register(DayOfWeek)
admin.site.register(CustomUser)
admin.site.register(Groups)
admin.site.register(Student)
admin.site.register(Teacher)


