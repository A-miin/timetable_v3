from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import View

from webapp.models import Teacher, TimeTable, TimeDay, TimeHour, Department


def home(request):
    return render(request, 'index.html')


class ListTimeTable(object):
    def __init__(self, course, classroom,course_type, teacher, department, time_day_id, time_hour_id):
        if course:
            self.course = course
            self.classroom = classroom
            self.teacher = teacher
            self.course_type = course_type
            self.department = department

        else:
            self.course = None
            self.classroom = None
            self.teacher = None
            self.course_type = None
            self.department = None

        self.time_day_id = time_day_id
        self.time_hour_id = time_hour_id



class TeacherTimeTableView(View):
    template_name = 'teacher.html'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return render(request, self.template_name, context={'teachers': queryset})

    def post(self, request, *args, **kwargs):
        teacher_id = self.request.POST.get('teacher', 0)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        timetable = TimeTable.objects.filter(course__teacher=teacher).order_by('time_hour_id', 'time_day_id')
        days, hours, index = TimeDay.objects.all().order_by('pk'), TimeHour.objects.all().order_by('pk'), 0
        result = []
        for hour in hours:
            for day in days:
                if index < len(timetable) and timetable[index].time_hour_id == hour.id and timetable[index].time_day_id == day.id:
                    while index < len(timetable) and timetable[index].time_hour_id == hour.id and timetable[index].time_day_id == day.id:
                        table = timetable[index]
                        if result:
                            if result[-1].time_day_id == table.time_day_id and result[-1].time_hour_id == table.time_hour_id:
                                result[-1].classroom += f', {table.classroom}'
                                index += 1
                            else:
                                result.append(ListTimeTable(course=f'{table.course.code} {table.course.name}',
                                                            classroom=str(table.classroom), teacher=table.course.teacher.name,
                                                            department=table.course.department.name,
                                                            course_type=table.course.type.type_code,
                                                            time_day_id=table.time_day_id, time_hour_id=table.time_hour_id))
                                index += 1
                        else:
                            result.append(ListTimeTable(course=f'{table.course.code} {table.course.name}',
                                                        classroom=str(table.classroom),
                                                        course_type=table.course.type.type_code,
                                                        teacher=table.course.teacher.name,
                                                        department=table.course.department.name,
                                                        time_day_id=table.time_day_id,
                                                        time_hour_id=table.time_hour_id))
                            index += 1
                else:
                    result.append(ListTimeTable(course=None,
                                                classroom=None,
                                                teacher=None,
                                                course_type=None,
                                                department=None,
                                                time_day_id=day.id,
                                                time_hour_id=hour.id))

        queryset = self.get_queryset()

        return render(request, self.template_name, context={'teachers': queryset, 'timetable': result,
                                                            'selected_teacher': teacher,
                                                            'days': days, 'hours': hours})

    def get_queryset(self):
        return Teacher.objects.all().order_by('name')

class DepartmentView(View):
    template_name = 'department.html'

    def get(self, request, *args, **kwargs):
        departments = self.get_departments()
        return render(request, self.template_name, context={'departments': departments})

    def post(self, request, *args, **kwargs):
        department_id = self.request.POST.get('department', 0)
        department = get_object_or_404(Department, id=department_id)
        timetable = TimeTable.objects.filter(course__department=department).order_by('time_hour_id', 'time_day_id')
        days, hours, index = TimeDay.objects.all().order_by('pk'), TimeHour.objects.all().order_by('pk'), 0
        result = []
        for table in timetable:
            print(table.course)

        departments = self.get_departments()

        return render(request, self.template_name, context={'departments': departments, 'timetable': result,
                                                            'selected_department': department,
                                                            'days': days, 'hours': hours})

    def get_departments(self):
        return Department.objects.all().order_by('name')

