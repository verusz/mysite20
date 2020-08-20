from django.contrib import admin

# Register your models here.
from django.db import models

from .models import Topic, Course, Student, Order


class StudentAdmin(admin.ModelAdmin):
    CITY_CHOICES = [
        ('WS', 'Windsor'),
        ('CG', 'Calgery'),
        ('MR', 'Montreal'),
        ('VC', 'Vancouver')
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        students = Student.objects
        return "City:{}, first_name: {}, last_name: {}".format(self.city, self.first_name, self.last_name)

    def upper_case_name(self):
        return self.first_name, self.last_name


class CourseAdmin(admin.ModelAdmin):
    """ show the name, topic, price, hours, and for_everyone fields """
    courses = Course.objects.all()

    def __str__(self):
        return ""

    @staticmethod
    def add_50_to_hours(course_name):
        course = Course.objects.get(name=course_name)
        course.hours += 10
        course.save()


# Register your models here.
admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Order)
# admin.site.register(StudentAdmin)

