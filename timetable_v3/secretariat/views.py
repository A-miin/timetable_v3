
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import View
from django.urls import reverse

from secretariat.forms import ClassRoomForm, TeacherForm, GradeYearForm, CourseForm, CourseVsRoomForm
from webapp.models import ClassRoom, Teacher, GradeYear, Course, CourseVsRoom, Building, TimeTable, TimeDay, TimeHour
from webapp.views import ListTimeTable
from django.db import models
from django.db.models import Count, F, Q, Sum

class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('secretariat:class_room_timetable')


class CustomLogoutView(LogoutView):
    next_page = 'secretariat:login'


class ClassRoomTimeTableView(View):
    template_name = 'classroom/timetable.html'

    def get(self, request, *args, **kwargs):
        building_short_names = Building.objects.order_by('short_name')
        rooms = self.get_rooms()
        return render(request, self.template_name, context={'rooms': rooms,'building_short_names':building_short_names })

    def post(self, request, *args, **kwargs):

        building_short_names = Building.objects.order_by('short_name')
        room_id = self.request.POST.get('room', 0)
        room = get_object_or_404(ClassRoom, id=room_id)
        timetable = TimeTable.objects.select_related('classroom', 'classroom__building', 'course', 'course__teacher',
                                                     'course__type', 'course__department', 'course__department__faculty',
                                                     'classroom__building', ).\
            filter(classroom=room).order_by('time_hour_id', 'time_day_id')
        unused_courses = Course.objects.annotate(used_count=Count('timetable', distinct=True, )).\
            annotate(max_used_count=F('practice_hours') +  F('theory_hours'),).filter(rooms__classroom_id=room.id).\
            distinct()
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
                                                            'days': days, 'hours': hours, 'building_short_names':building_short_names,
                                                            'unused_courses': unused_courses})

    def get_rooms(self):
        return ClassRoom.objects.select_related('building').all().order_by('building__short_name')




class ListClassRoomView(ListView):
    template_name = 'classroom/list.html'
    context_object_name = 'classrooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListClassRoomView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['classrooms'])
        return context

    def get_queryset(self):
        return ClassRoom.objects.select_related('building', 'room_type', 'department').filter(user_id=self.request.user.id)


class CreateClassRoomView(CreateView):
    form_class = ClassRoomForm
    template_name = 'classroom/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateClassRoomView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_class_room')


class UpdateClassRoomView(UpdateView):
    form_class = ClassRoomForm
    template_name = 'classroom/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ClassRoom, id=self.kwargs.get('id', 0))

    def get_form_kwargs(self):
        kwargs = super(UpdateClassRoomView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_class_room')


class DeleteClassRoomView(DeleteView):
    template_name = 'partial/delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ClassRoom, id=self.kwargs.get('id', 0))

    def get_success_url(self):
        return reverse('secretariat:list_class_room')


class ListTeacherView(ListView):
    template_name = 'teacher/list.html'
    context_object_name = 'teachers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListTeacherView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['teachers'])
        return context

    def get_queryset(self):
        return Teacher.objects.filter(user_id=self.request.user.id).order_by('name')


class CreateTeacherView(CreateView):
    form_class = TeacherForm
    template_name = 'teacher/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateTeacherView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_teacher')


class UpdateTeacherView(UpdateView):
    form_class = TeacherForm
    template_name = 'teacher/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Teacher, id=self.kwargs.get('id', 0))

    def get_form_kwargs(self):
        kwargs = super(UpdateTeacherView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_teacher')


class DeleteTeacherView(DeleteView):
    template_name = 'partial/delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Teacher, id=self.kwargs.get('id', 0))

    def get_success_url(self):
        return reverse('secretariat:list_teacher')


class ListGradeYearView(ListView):
    template_name = 'grade_year/list.html'
    context_object_name = 'grade_years'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListGradeYearView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['grade_years'])
        return context

    def get_queryset(self):
        faculty = self.request.user.faculty.faculty
        return GradeYear.objects.select_related('department').filter(department__faculty_id=faculty.id)


class CreateGradeYearView(CreateView):
    form_class = GradeYearForm
    template_name = 'grade_year/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateGradeYearView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_grade_year')


class UpdateGradeYearView(UpdateView):
    form_class = GradeYearForm
    template_name = 'grade_year/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(GradeYear, id=self.kwargs.get('id', 0))

    def get_form_kwargs(self):
        kwargs = super(UpdateGradeYearView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_grade_year')


class DeleteGradeYearView(DeleteView):
    template_name = 'partial/delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(GradeYear, id=self.kwargs.get('id', 0))

    def get_success_url(self):
        return reverse('secretariat:list_grade_year')


class ListCourseView(ListView):
    template_name = 'course/list.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListCourseView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['courses'])
        return context

    def get_queryset(self):
        return Course.objects.select_related('teacher', 'department',
                                             'practice_room_type', 'theory_room_type', 'type') \
                   .filter(user_id=self.request.user.id)


class CreateCourseView(CreateView):
    form_class = CourseForm
    template_name = 'course/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateCourseView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_course')


class UpdateCourseView(UpdateView):
    form_class = CourseForm
    template_name = 'course/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, id=self.kwargs.get('id', 0))

    def get_form_kwargs(self):
        kwargs = super(UpdateCourseView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_course')


class DeleteCourseView(DeleteView):
    template_name = 'partial/delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, id=self.kwargs.get('id', 0))

    def get_success_url(self):
        return reverse('secretariat:list_course')


class ListCourseVsRoomView(ListView):
    template_name = 'coursevsroom/list.html'
    context_object_name = 'coursevsrooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListCourseVsRoomView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['coursevsrooms'])
        return context

    def get_queryset(self):
        return CourseVsRoom.objects.select_related('course', 'classroom', 'classroom__building').filter(user_id=self.request.user.id)


class CreateCourseVsRoomView(CreateView):
    form_class = CourseVsRoomForm
    template_name = 'coursevsroom/create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateCourseVsRoomView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_course_vs_room')


class UpdateCourseVsRoomView(UpdateView):
    form_class = CourseVsRoomForm
    template_name = 'coursevsroom/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(CourseVsRoom, id=self.kwargs.get('id', 0))

    def get_form_kwargs(self):
        kwargs = super(UpdateCourseVsRoomView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('secretariat:list_course_vs_room')


class DeleteCourseVsRoomView(DeleteView):
    template_name = 'partial/delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(CourseVsRoom, id=self.kwargs.get('id', 0))

    def get_success_url(self):
        return reverse('secretariat:list_course_vs_room')

