from django.urls import path
from .views import home, TeacherTimeTableView

urlpatterns = [
    path('',home),
    path('teacher/', TeacherTimeTableView.as_view(), name='teacher_list')
]
