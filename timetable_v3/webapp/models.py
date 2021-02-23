from django.contrib.auth.models import User
from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, db_column='shortName')
    distance_number = models.IntegerField(db_column='distanceNumber')

    class Meta:
        db_table = 'building'


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    building = models.ForeignKey(to=Building, related_name='faculties', default=None, null=True, blank=True)

    class Meta:
        db_table = 'faculty'


class UserFaculty(models.Model):
    user = models.OneToOneField(to=User, related_name='faculty', on_delete=models.CASCADE)
    faculty = models.ForeignKey(to=Faculty, related_name='user_faculties', on_delete=models.CASCADE)


class Department(models.Model):
    faculty = models.ForeignKey(to=Faculty, related_name='departments', default=None, null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'department'


class RoomType(models.Model):
    type = models.CharField(max_length=255)
    type_code = models.IntegerField(db_column='typeCode')

    class Meta:
        db_table = 'room_type'


class Teacher(models.Model):
    user = models.ForeignKey(to=User, related_name='teachers', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.IntegerField(unique=True, db_column='sicil')
    name = models.CharField(max_length=255)
    unvan = models.CharField(max_length=255, db_column='unvan')
    extra_data = models.CharField(max_length=255, db_column='extraData')
    employee_type = models.IntegerField(db_column='employeeType')

    class Meta:
        db_table = 'teacher'


class ClassRoom(models.Model):
    building = models.ForeignKey(to=Building, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    name= models.CharField(max_length=255)
    capacity = models.IntegerField()
    room_type = models.ForeignKey(to=RoomType, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True, db_column='roomType_id')


    class Meta:
        db_table = 'classroom'


class CourseType(models.Model):
    type = models.CharField(max_length=255)
    type_code = models.IntegerField(db_column='typeCode')

    class Meta:
        db_table = 'course_type'


class Course(models.Model):
    teacher = models.ForeignKey(to=Teacher, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(to=Department, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    theory_hours = models.IntegerField(db_column='teorikDersSaati')
    practice_hours = models.IntegerField(db_column='uygulamaDersSaati')
    max_students = models.IntegerField(db_column='maxOgrenciSayisi')
    code = models.CharField(max_length=255, db_column='dersKodu')
    name = models.CharField(max_length=255, db_column='dersAdi')
    type = models.ForeignKey(to=CourseType, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True, db_column='courseType_id')
    theory_room_type = models.ForeignKey(to=RoomType, related_name='theory_courses', on_delete=models.SET_NULL, null=True, blank=True, db_column='teorikRoomType_id')
    practice_room_type = models.ForeignKey(to=RoomType, related_name='practice_courses',on_delete=models.SET_NULL, null=True, blank=True, db_column='uygulamaRoomType_id')
    credits = models.IntegerField(db_column='kredi')
    # TODO EDIT
    etkin = models.IntegerField(db_column='etkin')
    sube = models.IntegerField(db_column='sube')
    unpositioned_theory_hours = models.IntegerField(db_column='unpositionedTeorikHours')
    unpositioned_practice_hours = models.IntegerField(db_column='unpositionedUygulamaHours')
    semester = models.CharField(max_length=255)

    class Meta:
        db_table = 'course'


class CourseVsRoom(models.Model):
    course = models.ForeignKey(to=Course, related_name='rooms', on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, related_name='course_vs_rooms', on_delete=models.SET_NULL, null=True, blank=True)
    lesson_type = models.IntegerField(db_column='lessonType')

    class Meta:
        db_table = 'course_vs_room'


class GradeYear(models.Model):
    department = models.ForeignKey(to=Department, related_name='grade_years', on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.IntegerField()

    class Meta:
        db_table = 'grade_year'


class TimeTableGenerator(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(to=ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    grade_year = models.ForeignKey(to=GradeYear, on_delete=models.SET_NULL, null=True, blank=True, db_column='gradeYear_id')
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'ders_plan_generator'


class Editor(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    old_time = models.IntegerField(db_column='oldtime')
    new_time = models.IntegerField(db_column='new_time')
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'editor'


class TimeDay(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column='idtimeDay')
    order_position = models.IntegerField(db_column='orderPosition', null=True, blank=True)
    label = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'timeDay'


class TimeHour(models.Model):
    order_position = models.IntegerField(db_column='orderPosition', null=True, blank=True)
    label = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'timeHour'


class TimeTable(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    time_day = models.ForeignKey(to=TimeDay, on_delete=models.SET_NULL, null=True, blank=True)
    time_hour = models.ForeignKey(to=TimeHour, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField(db_column='yil')
    semester = models.CharField(max_length=45)

    class Meta:
        db_table = 'timeTable'
