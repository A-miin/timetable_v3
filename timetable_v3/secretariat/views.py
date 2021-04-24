
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from django.urls import reverse

from secretariat.forms import ClassRoomForm, TeacherForm, GradeYearForm
from webapp.models import ClassRoom, Teacher, GradeYear


class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('secretariat:timetable')


class CustomLogoutView(LogoutView):
    next_page = 'secretariat:login'


class TimeTableView(TemplateView):
    template_name = 'timetable.html'


class ListClassRoomView(ListView):
    template_name = 'classroom/list.html'
    context_object_name = 'classrooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListClassRoomView, self).get_context_data(**kwargs)
        context['total_count'] = len(context['classrooms'])
        return context

    def get_queryset(self):
        return ClassRoom.objects.filter(user_id=self.request.user.id)


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
        return GradeYear.objects.filter(department__faculty_id=faculty.id)


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


