from operator import itemgetter

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import View

from webapp.models import Teacher, TimeTable, TimeDay, TimeHour, Department, ClassRoom, Building, Faculty


def home(request):
    return render(request, 'index.html')


class ListTimeTable(object):
    def __init__(self, time_day_id, time_hour_id, course=None, classroom=None,course_type=None, teacher=None, department=None, faculty=None):
        self.course = course
        self.classroom = classroom
        self.teacher = teacher
        self.course_type = course_type
        self.department = department
        self.faculty = faculty
        self.time_day_id = time_day_id
        self.time_hour_id = time_hour_id

    def is_empty(self):
        return self.classroom is None

    def get_values(self, table: TimeTable):
        if self.classroom is None:
            self.course = table.course.full_name
            self.course_type = table.course.type.type_code
            if self.course_type != 5:
                self.teacher = table.course.teacher.name
                self.classroom = table.classroom.short_name
                self.department = table.course.department.name
                self.faculty = table.course.department.faculty.name
        else:

            self.classroom += f', {table.classroom.short_name}'



class TeacherTimeTableView(View):
    template_name = 'teacher.html'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return render(request, self.template_name, context={'teachers': queryset})

    def post(self, request, *args, **kwargs):
        rooms = ClassRoom.objects.order_by('building__short_name')
        teacher_id = self.request.POST.get('teacher',0)
        teacher_code = self.request.POST.get('teacher_number',0)
        if teacher_code=='':
            teacher = get_object_or_404(Teacher, id=teacher_id)
        else:
            teacher = get_object_or_404(Teacher, code=int(teacher_code))
        timetable = TimeTable.objects.filter(course__teacher=teacher).order_by('time_hour_id', 'time_day_id')
        days, hours, index = TimeDay.objects.all().order_by('pk'), TimeHour.objects.all().order_by('pk'), 0
        result = [ListTimeTable(time_day_id=day.id, time_hour_id=hour.id) for hour in hours for day in days]
        for table in result:
            while index < len(timetable) and timetable[index].time_hour_id == table.time_hour_id and \
                    timetable[index].time_day_id == table.time_day_id:
                table.get_values(timetable[index])
                index += 1
        queryset = self.get_queryset()

        return render(request, self.template_name, context={'teachers': queryset, 'timetable': result,
                                                            'selected_teacher': teacher,
                                                            'days': days, 'hours': hours, 'teacher_code':teacher_code})

    def get_queryset(self):
        return Teacher.objects.all().order_by('name')

class DepartmentView(View):
    template_name = 'department.html'

    def get(self, request, *args, **kwargs):
        departments = self.get_departments()
        faculties = Faculty.objects.all().order_by("name")
        return render(request, self.template_name, context={'departments': departments, 'faculties':faculties})

    def post(self, request, *args, **kwargs):
        department_id = self.request.POST.get('department', 0)
        department = get_object_or_404(Department, id=department_id)
        grades = department.grade_years.all().values_list('grade', flat=True).order_by('grade')

        timetable = TimeTable.objects.\
            filter(course__department=department).select_related('course', 'course__department', 'course__teacher',
                                                                 'course__department__faculty', 'classroom',
                                                                 'course__type', 'classroom__building').\
            order_by('course__year','time_hour_id', 'time_day_id')
        days, hours, index = TimeDay.objects.all().order_by('pk'), TimeHour.objects.all().order_by('pk'), 0
        years = {grade: [] for grade in grades}
        for table in timetable:
            years[table.course.year].append(table)
        result = {}
        for year, timetable in years.items():
            temp_result = [{'first':ListTimeTable(time_day_id=day.id, time_hour_id=hour.id),
                            'second':ListTimeTable(time_day_id=day.id, time_hour_id=hour.id),
                            'third':ListTimeTable(time_day_id=day.id, time_hour_id=hour.id),
                            } for hour in hours for day in days]
            index = 0
            for table in temp_result:
                while index < len(timetable) and timetable[index].time_hour_id == table['first'].time_hour_id and \
                        timetable[index].time_day_id == table['first'].time_day_id:
                    if table['first'].is_empty():
                        table['first'].get_values(timetable[index])
                    elif table['second'].is_empty():
                        table['second'].get_values(timetable[index])
                    else:
                        table['third'].get_values(timetable[index])

                    index += 1
            result[year] = temp_result
        departments = self.get_departments()
        faculties = Faculty.objects.all().order_by("name")
        return render(request, self.template_name, context={'departments': departments, 'timetable': result,
                                                            'selected_department': department,
                                                            'days': days, 'hours': hours, 'faculties':faculties})

    def get_departments(self):
        return Department.objects.all().order_by('name')


class RoomView(View):
    template_name = 'classroom.html'


    def get(self, request, *args, **kwargs):
        building_short_names = Building.objects.order_by('short_name')
        rooms = self.get_rooms()
        return render(request, self.template_name, context={'rooms': rooms,'building_short_names':building_short_names })

    def post(self, request, *args, **kwargs):
        building_short_names = Building.objects.order_by('short_name')
        room_id = self.request.POST.get('room', 0)
        room = get_object_or_404(ClassRoom, id=room_id)
        timetable = TimeTable.objects.filter(classroom=room).order_by('time_hour_id', 'time_day_id')
        days, hours, index = TimeDay.objects.all().order_by('pk'), TimeHour.objects.all().order_by('pk'), 0
        result = [ListTimeTable(time_day_id=day.id, time_hour_id=hour.id) for hour in hours for day in days]
        for table in result:
            while index < len(timetable) and timetable[index].time_hour_id == table.time_hour_id and \
                    timetable[index].time_day_id == table.time_day_id:
                table.get_values(timetable[index])
                index += 1

        rooms = self.get_rooms()

        return render(request, self.template_name, context={'rooms': rooms, 'timetable': result,
                                                            'selected_room': room,'selected_building_short': room.building.short_name,
                                                            'days': days, 'hours': hours, 'building_short_names':building_short_names})

    def get_rooms(self):
        return ClassRoom.objects.all().order_by('building__short_name')
