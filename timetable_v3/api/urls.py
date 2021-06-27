from django.urls import path

from api.views import TimeTableView, ReserveClassRoomView, ReserveGradeYearView, FacultyView, DepartmentView, \
    CourseTimeTableView, ReserveTeacherView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = 'api'
schema_view = get_schema_view(
    openapi.Info(
        title="Manas TimeTable API documentation",
        default_version='v1',
        description="Manas TimeTable",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('timetable/', TimeTableView.as_view(), name='timetable'),
    path('reserve/classroom/', ReserveClassRoomView.as_view(), name='reserve_classroom'),
    path('reserve/teacher/', ReserveTeacherView.as_view(), name='reserve_classroom'),
    path('reserve/grade_year/', ReserveGradeYearView.as_view(), name='reserve_classroom'),
    path('faculty/', FacultyView.as_view(), name='faculty_list'),
    path('deparment/', DepartmentView.as_view(), name='department_list'),
    path('course/', CourseTimeTableView.as_view(), name='course_detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]
