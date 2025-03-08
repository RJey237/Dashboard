from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class UserTypeEnum(models.TextChoices):
        ADMIN = 'admin'
        TEACHER = 'teacher'
        STUDENT = 'student'

    user_type = models.CharField(max_length=100, choices=UserTypeEnum.choices, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    linkedin_url = models.CharField(blank=True, null=True)
    telegram_url = models.CharField(max_length=255, blank=True, null=True)
    instagram_url = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = ("Profiles")

    def __str__(self):
        return self.username

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''


class DayOfWeek(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Day of Week"
        verbose_name_plural = "Days of Week"
        ordering = ['name']


class Groups(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    days_of_week = models.ManyToManyField(DayOfWeek,
                                            help_text=("Days of the week for this group."))
    start_time = models.TimeField(help_text=("Start time for this lesson (e.g., 19:00 for 7 PM)."))
    end_time = models.TimeField(help_text=("End time for this lesson (e.g., 21:00 for 9 PM)."))

    class Meta:
        verbose_name = ("Group")
        verbose_name_plural = ("Groups")
        ordering = ['start_time']

    def __str__(self):
        days = ", ".join(day.name for day in self.days_of_week.all())
        return f"{self.title}: {days} {self.start_time:%H:%M} - {self.end_time:%H:%M}"


class Student(models.Model):  # No inheritance from AbstractUser
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)  # Optional
    enrollment_date = models.DateField(null=True, blank=True)  # Optional
    father_fullname = models.CharField(max_length=100, blank=True, null=True)
    father_phone_number = models.CharField(max_length=20, blank=True, null=True)
    mother_fullname = models.CharField(max_length=100, blank=True, null=True)
    mother_phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.student.username #Now it will work correctly.


class Teacher(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recruitment_date = models.DateField()