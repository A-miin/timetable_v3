from django.urls import path

from secretariat.views import ClassRoomTimeTableView, CustomLoginView, CustomLogoutView, ListClassRoomView, \
    CreateClassRoomView, \
    UpdateClassRoomView, DeleteClassRoomView, ListTeacherView, CreateTeacherView, UpdateTeacherView, DeleteTeacherView, \
    ListGradeYearView, CreateGradeYearView, UpdateGradeYearView, DeleteGradeYearView, ListCourseView, CreateCourseView, \
    UpdateCourseView, DeleteCourseView, ListCourseVsRoomView, DeleteCourseVsRoomView, UpdateCourseVsRoomView, \
    CreateCourseVsRoomView, TimeTableActionsView, ReserveClassRoomView, ReserveTeacherView

app_name = 'secretariat'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('timetable/', ClassRoomTimeTableView.as_view(), name='class_room_timetable'),
    path('api/timetable/', TimeTableActionsView.as_view(), name='api_timetable'),
    path('classrooms/', ListClassRoomView.as_view(), name='list_class_room'),
    path('classroom/create/', CreateClassRoomView.as_view(), name='create_class_room'),
    path('classroom/update/<int:id>/', UpdateClassRoomView.as_view(), name='update_class_room'),
    path('classroom/delete/<int:id>/', DeleteClassRoomView.as_view(), name='delete_class_room'),
    path('api/classroom/reserve/', ReserveClassRoomView.as_view(), name='reserve_classroom'),
    path('api/teacher/reserve/', ReserveTeacherView.as_view(), name='reserve_teacher'),
    path('teachers/', ListTeacherView.as_view(), name='list_teacher'),
    path('teacher/create/', CreateTeacherView.as_view(), name='create_teacher'),
    path('teacher/update/<int:id>/', UpdateTeacherView.as_view(), name='update_teacher'),
    path('teacher/delete/<int:id>/', DeleteTeacherView.as_view(), name='delete_teacher'),
    path('grade_years/', ListGradeYearView.as_view(), name='list_grade_year'),
    path('grade_year/create/', CreateGradeYearView.as_view(), name='create_grade_year'),
    path('grade_year/update/<int:id>/', UpdateGradeYearView.as_view(), name='update_grade_year'),
    path('grade_year/delete/<int:id>/', DeleteGradeYearView.as_view(), name='delete_grade_year'),
    path('courses/', ListCourseView.as_view(), name='list_course'),
    path('course/create/', CreateCourseView.as_view(), name='create_course'),
    path('course/update/<int:id>/', UpdateCourseView.as_view(), name='update_course'),
    path('course/delete/<int:id>/', DeleteCourseView.as_view(), name='delete_course'),
    path('coursevsrooms/', ListCourseVsRoomView.as_view(), name='list_course_vs_room'),
    path('coursevsroom/create/', CreateCourseVsRoomView.as_view(), name='create_course_vs_room'),
    path('coursevsroom/update/<int:id>/', UpdateCourseVsRoomView.as_view(), name='update_course_vs_room'),
    path('coursevsroom/delete/<int:id>/', DeleteCourseVsRoomView.as_view(), name='delete_course_vs_room'),
]
