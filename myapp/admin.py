from django.contrib import admin

# Register your models here.
from django.db import models

from .models import Topic, Course, Student, Order


def upper_case_name(student):
    return ("%s, %s" % (student.first_name, student.last_name)).upper()


def city(student):
    return ("%s" % student.city).upper()


upper_case_name.short_description = 'Student Full Name'


class StudentAdmin(admin.ModelAdmin):
    list_display = (upper_case_name, city)


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
# admin.site.register(Student)
admin.site.register(Order)
admin.site.register(Student, StudentAdmin)
