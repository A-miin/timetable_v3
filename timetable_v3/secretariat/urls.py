from django.urls import path

from secretariat.views import TimeTableView, CustomLoginView, CustomLogoutView, ListClassRoomView, CreateClassRoomView, \
    UpdateClassRoomView, DeleteClassRoomView, ListTeacherView, CreateTeacherView, UpdateTeacherView, DeleteTeacherView, \
    ListGradeYearView, CreateGradeYearView, UpdateGradeYearView, DeleteGradeYearView

app_name = 'secretariat'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('timetable/', TimeTableView.as_view(), name='timetable'),
    path('classrooms/', ListClassRoomView.as_view(), name='list_class_room'),
    path('classroom/create/', CreateClassRoomView.as_view(), name='create_class_room'),
    path('classroom/update/<int:id>/', UpdateClassRoomView.as_view(), name='update_class_room'),
    path('classroom/delete/<int:id>/', DeleteClassRoomView.as_view(), name='delete_class_room'),
    path('teachers/', ListTeacherView.as_view(), name='list_teacher'),
    path('teacher/create/', CreateTeacherView.as_view(), name='create_teacher'),
    path('teacher/update/<int:id>/', UpdateTeacherView.as_view(), name='update_teacher'),
    path('teacher/delete/<int:id>/', DeleteTeacherView.as_view(), name='delete_teacher'),
    path('grade_years/', ListGradeYearView.as_view(), name='list_grade_year'),
    path('grade_year/create/', CreateGradeYearView.as_view(), name='create_grade_year'),
    path('grade_year/update/<int:id>/', UpdateGradeYearView.as_view(), name='update_grade_year'),
    path('grade_year/delete/<int:id>/', DeleteGradeYearView.as_view(), name='delete_grade_year'),
]
