from django.urls import path
from .views import home, TeacherTimeTableView, DepartmentView, RoomView

urlpatterns = [
    path('',home),
    path('teacher/', TeacherTimeTableView.as_view(), name='teacher_list'),
    path('department/', DepartmentView.as_view(), name='department_list'),
    path('room/', RoomView.as_view(), name='room_list'),
]
