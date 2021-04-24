
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.urls import reverse


class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('secretariat:timetable')


class CustomLogoutView(LogoutView):
    next_page = 'secretariat:login'


class TimeTableView(TemplateView):
    template_name = 'timetable.html'
