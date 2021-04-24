from django.contrib import admin
from .models import Department, Faculty, Building, RoomType, Teacher, ClassRoom, CourseType, Editor, Course, \
    CourseVsRoom, GradeYear, TimeTableGenerator, TimeDay, TimeHour, TimeTable, UserFaculty


admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(UserFaculty)
admin.site.register(RoomType)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Building)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(CourseVsRoom)
admin.site.register(GradeYear)
admin.site.register(TimeTableGenerator)
admin.site.register(Editor)
admin.site.register(TimeDay)
admin.site.register(TimeHour)
admin.site.register(TimeTable)
# Register your models here.
