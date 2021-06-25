from django.contrib import admin
from .models import Department, Faculty, Building, RoomType, Teacher, ClassRoom, CourseType, Course, \
    CourseVsRoom, GradeYear, TimeDay, TimeHour, TimeTable, UserFaculty
from django.db.models import Q
from model_clone import CloneModelAdmin
TIMETABLE_RESERVED = 'reserved'

class TimeTableAdmin(CloneModelAdmin):
    list_filter = ('course__department__name', )
    search_fields = ['course__name', 'classroom__name', 'course__teacher__name']
    list_display = ['id', 'course','classroom', 'time_hour','time_day']

    model = TimeTable
    def get_queryset(self, request):
        return TimeTable.objects.exclude(Q(course__name=TIMETABLE_RESERVED) | Q(classroom__name=TIMETABLE_RESERVED) |
                                         Q(course__teacher__name=TIMETABLE_RESERVED) | Q(classroom__isnull=True) |
                                         Q(course__isnull=True) | Q(course__teacher__isnull=True))

class CourseAdmin(CloneModelAdmin):
    model = Course
    search_fields = ['name', 'code', 'teacher__name']
    list_filter = ('department__name',)
    list_display = ['id','code', 'name', 'teacher', 'department']

class ClassRoomAdmin(CloneModelAdmin):
    model = ClassRoom
    search_fields = ['name', 'building__short_name', 'building__name']
    list_filter = ('building__name',)
    list_display = ['id', 'name', 'building', 'capacity', 'room_type']

class TeacherAdmin(CloneModelAdmin):
    model = Teacher
    search_fields = ['name', 'code']
    list_filter = ('courses__department__name',)
    list_display = ['id', 'code', 'name', 'unvan','employee_type']


admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(UserFaculty)
admin.site.register(RoomType)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Building)
admin.site.register(CourseType)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseVsRoom)
admin.site.register(GradeYear)
admin.site.register(TimeDay)
admin.site.register(TimeHour)
admin.site.register(TimeTable, TimeTableAdmin)
# Register your models here.
