from django.urls import path

from secretariat.views import TimeTableView, CustomLoginView, CustomLogoutView

app_name = 'secretariat'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('timetable/', TimeTableView.as_view(), name='timetable')
]
