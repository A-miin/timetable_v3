from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import View

from webapp.models import Teacher, TimeTable


def home(request):
    return render(request, 'index.html')


class TeacherTimeTableView(View):
    template_name = 'teacher.html'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return render(request, self.template_name, context={'teachers': queryset})

    def post(self, request, *args, **kwargs):
        teacher_id = self.request.POST.get('teacher', 0)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        timetable = TimeTable.objects.filter(course__teacher=teacher).order_by('time_day_id', 'time_hour_id')
        queryset = self.get_queryset()

        return render(request, self.template_name, context={'teachers': queryset, 'timetable': timetable,
                                                            'selected_teacher': teacher.id, })

    def get_queryset(self):
        return Teacher.objects.all().order_by('name')

