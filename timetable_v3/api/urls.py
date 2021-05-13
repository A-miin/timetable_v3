from django.urls import path

from api.views import TimeTableView, ReserveClassRoomView, ReserveGradeYearView

app_name = 'api'

urlpatterns = [
    path('timetable/', TimeTableView.as_view(), name='timetable'),
    path('reserve/classroom/', ReserveClassRoomView.as_view(), name='reserve_classroom'),
    path('reserve/teacher/', ReserveClassRoomView.as_view(), name='reserve_classroom'),
    path('reserve/grade_year/', ReserveGradeYearView.as_view(), name='reserve_classroom'),
]
