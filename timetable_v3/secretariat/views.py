
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from django.urls import reverse

from secretariat.forms import ClassRoomForm
from webapp.models import ClassRoom


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


