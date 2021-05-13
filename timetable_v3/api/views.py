from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.schemas import ErrorResponseAutoSchema
from api.serializers import CreateTimeTableSerializer, MoveTimeTableSerializer, DeleteTimeTableSerializer, \
    CreateReserveTeacherSerializer, DeleteReserveTeacherSerializer, CreateReserveClassRoomSerializer, \
    DeleteReserveClassRoomSerializer, DeleteReserveGradeYearSerializer, CreateReserveGradeYearSerializer, \
    DepartmentSerializer, FacultySerializer, CourseTimeTableSerializer
from webapp.models import Department, Faculty, Course, TimeTable


class ActionMixin:
    def actions(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class TimeTableView(ActionMixin, generics.GenericAPIView):
    swagger_schema = None
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTimeTableSerializer
        if self.request.method == 'PUT':
            return MoveTimeTableSerializer
        else:
            return DeleteTimeTableSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


class ReserveClassRoomView(ActionMixin, generics.GenericAPIView):
    swagger_schema = None
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveClassRoomSerializer
        return DeleteReserveClassRoomSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


class ReserveTeacherView(ActionMixin, generics.GenericAPIView):
    swagger_schema = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveTeacherSerializer
        return DeleteReserveTeacherSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


class ReserveGradeYearView(ActionMixin, generics.GenericAPIView):
    swagger_schema = None
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveGradeYearSerializer
        return DeleteReserveGradeYearSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


@method_decorator(name='get', decorator=swagger_auto_schema(
    auto_schema=ErrorResponseAutoSchema,
    operation_description="List all departments of Manas university.",
    operation_id='List Department Endpoint',
    manual_parameters=[openapi.Parameter('faculty_id', openapi.IN_QUERY, description="Filter by faculty",
                                         type=openapi.TYPE_INTEGER, required=False)],
    tags=['Open Endpoints']
))
class DepartmentView(generics.ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        qs = Department.objects.all().order_by('name')
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        return qs

@method_decorator(name='get', decorator=swagger_auto_schema(
    auto_schema=ErrorResponseAutoSchema,
    operation_description="List all faculties of Manas university.",
    operation_id='List Faculty Endpoint',
    tags=['Open Endpoints']
))
class FacultyView(generics.ListAPIView):
    serializer_class = FacultySerializer

    def get_queryset(self):
        return Faculty.objects.all().order_by('name')


@method_decorator(name='get', decorator=swagger_auto_schema(
    auto_schema=ErrorResponseAutoSchema,
    operation_description="Get detailed information of course.",
    operation_id='Get Course Endpoint',
    tags=['Open Endpoints']
))
class CourseTimeTableView(generics.RetrieveAPIView):
    serializer_class = CourseTimeTableSerializer

    def get_object(self):
        code = self.request.GET.get('code')
        return Course.objects.select_related('department', 'department__faculty', 'teacher', 'type').\
            prefetch_related(Prefetch('timetable_set',queryset=TimeTable.objects.select_related('time_day', 'time_hour', 'classroom', 'classroom__building'))).filter(code=code).first()