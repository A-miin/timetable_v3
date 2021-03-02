from django.urls import path
from .views import home, TeacherTimeTableView, DepartmentView

urlpatterns = [
    path('',home),
    path('teacher/', TeacherTimeTableView.as_view(), name='teacher_list'),
    path('department/', DepartmentView.as_view(), name='department_list')
]
