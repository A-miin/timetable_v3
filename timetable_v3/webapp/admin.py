from django.contrib import admin
from .models import Department, Faculty, Building, RoomType, Teacher, ClassRoom, CourseType, Editor, Course, \
    CourseVsRoom, GradeYear, TimeTableGenerator, TimeDay, TimeHour, TimeTable, UserFaculty
from django.db.models import Q

TIMETABLE_RESERVED = 'reserved'

class TimeTableAdmin(admin.ModelAdmin):
    model = TimeTable
    def get_queryset(self, request):
        return TimeTable.objects.exclude(Q(course__name=TIMETABLE_RESERVED) | Q(classroom__name=TIMETABLE_RESERVED) |
                                         Q(course__teacher__name=TIMETABLE_RESERVED) | Q(classroom__isnull=True) |
                                         Q(course__isnull=True) | Q(course__teacher__isnull=True))
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
admin.site.register(TimeTable, TimeTableAdmin)
# Register your models here.
