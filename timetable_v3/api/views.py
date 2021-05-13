from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CreateTimeTableSerializer, MoveTimeTableSerializer, DeleteTimeTableSerializer, \
    CreateReserveTeacherSerializer, DeleteReserveTeacherSerializer, CreateReserveClassRoomSerializer, \
    DeleteReserveClassRoomSerializer, DeleteReserveGradeYearSerializer, CreateReserveGradeYearSerializer


class ActionMixin:
    def actions(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class TimeTableView(ActionMixin, generics.GenericAPIView):

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
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveClassRoomSerializer
        return DeleteReserveClassRoomSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


class ReserveTeacherView(ActionMixin, generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveTeacherSerializer
        return DeleteReserveTeacherSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)


class ReserveGradeYearView(ActionMixin, generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReserveGradeYearSerializer
        return DeleteReserveGradeYearSerializer

    def post(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.actions(request, *args, **kwargs)
