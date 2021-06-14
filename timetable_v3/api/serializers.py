from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from webapp.models import TimeTable, ClassRoom, Teacher, GradeYear, Department, Faculty, Course


class DeleteTimeTableSerializer(serializers.Serializer):
    time_hour_day = serializers.IntegerField(required=True)
    course_id = serializers.IntegerField(required=True)
    classroom_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        day, hour = TimeTable.get_time_day_objects(time_hour_day=self.validated_data.pop('time_hour_day'))
        classroom_id, course_id = self.validated_data['classroom_id'], self.validated_data['course_id']
        TimeTable.objects.filter(course_id=course_id, time_day=day,
                                 classroom_id=classroom_id,time_hour=hour).delete()


class CreateTimeTableSerializer(serializers.Serializer):
    time_hour_day = serializers.IntegerField(required=True)
    course_id = serializers.IntegerField(required=True)
    classroom_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        day, hour = TimeTable.get_time_day_objects(time_hour_day=self.validated_data.pop('time_hour_day'))
        classroom_id, course_id = self.validated_data['classroom_id'], self.validated_data['course_id']
        if not TimeTable.objects.filter(classroom_id=classroom_id, time_day=day, time_hour=hour, course_id=course_id).exists():
            TimeTable.objects.create(classroom_id=classroom_id, time_day=day, time_hour=hour, course_id=course_id)


class MoveTimeTableSerializer(serializers.Serializer):
    old_time_hour_day = serializers.IntegerField(required=True)
    new_time_hour_day = serializers.IntegerField(required=True)
    course_id = serializers.IntegerField(required=True)
    classroom_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        old_day, old_hour = TimeTable.get_time_day_objects(time_hour_day=self.validated_data['old_time_hour_day'])
        new_day, new_hour = TimeTable.get_time_day_objects(time_hour_day=self.validated_data['new_time_hour_day'])
        classroom_id, course_id = self.validated_data['classroom_id'], self.validated_data['course_id']
        TimeTable.objects.filter(classroom_id=classroom_id, time_day=old_day, time_hour=old_hour, course_id=course_id) \
            .update(time_day=new_day, time_hour=new_hour)


class DeleteReserveClassRoomSerializer(serializers.Serializer):
    day_id = serializers.IntegerField(required=True)
    hour_id = serializers.IntegerField(required=True)
    classroom_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        day_id, hour_id, classroom_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['classroom_id']
        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        classroom.delete_reserved(day_id=day_id, hour_id=hour_id)


class CreateReserveClassRoomSerializer(DeleteReserveClassRoomSerializer):
    def save(self, **kwargs):
        day_id, hour_id, classroom_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['classroom_id']
        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        classroom.create_reserved(day_id=day_id, hour_id=hour_id)


class DeleteReserveTeacherSerializer(serializers.Serializer):
    day_id = serializers.IntegerField(required=True)
    hour_id = serializers.IntegerField(required=True)
    teacher_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        day_id, hour_id, teacher_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['teacher_id']
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.delete_reserved(day_id=day_id, hour_id=hour_id)


class CreateReserveTeacherSerializer(DeleteReserveTeacherSerializer):
    def save(self, **kwargs):
        day_id, hour_id, teacher_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['teacher_id']
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.create_reserved(day_id=day_id, hour_id=hour_id)


class DeleteReserveGradeYearSerializer(serializers.Serializer):
    day_id = serializers.IntegerField(required=True)
    hour_id = serializers.IntegerField(required=True)
    grade_year_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        day_id, hour_id, grade_year_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['grade_year_id']
        grade_year = get_object_or_404(GradeYear, id=grade_year_id)
        grade_year.delete_reserved(day_id=day_id, hour_id=hour_id)


class CreateReserveGradeYearSerializer(DeleteReserveGradeYearSerializer):
    def save(self, **kwargs):
        day_id, hour_id, grade_year_id = self.validated_data['day_id'], self.validated_data['hour_id'],\
                                        self.validated_data['grade_year_id']
        grade_year = get_object_or_404(GradeYear, id=grade_year_id)
        grade_year.create_reserved(day_id=day_id, hour_id=hour_id)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id',
                  'name')


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id',
                  'name')


class TimeTableSerializer(serializers.ModelSerializer):
    classroom = serializers.SerializerMethodField()
    time_day = serializers.SlugRelatedField(slug_field='label', read_only=True)
    time_hour = serializers.SlugRelatedField(slug_field='label', read_only=True)

    def get_classroom(self, instance: TimeTable):
        return f'{instance.classroom.building.short_name}-{instance.classroom.name}'

    class Meta:
        model = TimeTable
        fields = ('time_day',
                  'time_hour',
                  'classroom')


class CourseTimeTableSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    teacher = serializers.SlugRelatedField(slug_field='name', read_only=True)
    type = serializers.SlugRelatedField(slug_field='type', read_only=True)
    timetable = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=DepartmentSerializer)
    def get_department(self, instance: Course):
        return DepartmentSerializer(instance=instance.department).data

    @swagger_serializer_method(serializer_or_field=FacultySerializer)
    def get_faculty(self, instance: Course):
        return FacultySerializer(instance=instance.department.faculty).data

    @swagger_serializer_method(serializer_or_field=TimeTableSerializer)
    def get_timetable(self, instance: Course):
        return TimeTableSerializer(instance=instance.timetable_set.all().order_by('time_day_id', 'time_hour_id'),
                                   many=True).data

    class Meta:
        model = Course
        fields = ('faculty',
                  'department',
                  'teacher',
                  'timetable',
                  'type')
