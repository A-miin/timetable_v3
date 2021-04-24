from django.contrib.auth.models import User, AbstractUser
from django.db import models



class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, db_column='shortName')
    distance_number = models.IntegerField(db_column='distanceNumber')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'building'


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    building = models.ForeignKey(to=Building, related_name='faculties', on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'faculty'


class UserFaculty(models.Model):
    user = models.OneToOneField(to=User, related_name='faculty', on_delete=models.CASCADE)
    faculty = models.OneToOneField(to=Faculty, related_name='user_faculties', on_delete=models.CASCADE)


class Department(models.Model):
    faculty = models.ForeignKey(to=Faculty, related_name='departments', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'


class RoomType(models.Model):
    type = models.CharField(max_length=255, null=True)
    type_code = models.IntegerField(db_column='typeCode', null=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'room_type'


class Teacher(models.Model):
    user = models.ForeignKey(to=User, related_name='teachers', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.IntegerField(db_column='sicil', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    unvan = models.CharField(max_length=255, db_column='unvan', null=True, blank=True)
    extra_data = models.CharField(max_length=255, db_column='extraData', null=True, blank=True)
    employee_type = models.IntegerField(db_column='employeeType', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def type(self):
        if self.employee_type == 0:
            return 'Tam Zamanlı'
        elif self.employee_type == 1:
            return 'Yarı Zamanlı'
        else:
            return 'DSU'

    class Meta:
        db_table = 'teacher'


class ClassRoom(models.Model):
    building = models.ForeignKey(to=Building, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    name= models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    room_type = models.ForeignKey(to=RoomType, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True, db_column='roomType_id')

    def __str__(self):
        return f'{self.building.short_name}-{self.name} kapasitesi: {self.capacity}'

    @property
    def short_name(self):
        if self.building:
            return f'{self.building.short_name}-{self.name}'
        return self.name

    @property
    def full_name(self):
        if self.building:
            return f'{self.building.short_name} - {self.building.short_name}-{self.name} kapasitesi: {self.capacity}'
        return self.name

    class Meta:
        db_table = 'classroom'


class CourseType(models.Model):
    type = models.CharField(max_length=255, null=True)
    type_code = models.IntegerField(db_column='typeCode', null=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'course_type'


class Course(models.Model):
    teacher = models.ForeignKey(to=Teacher, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(to=Department, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    theory_hours = models.IntegerField(db_column='teorikDersSaati', null=True, blank=True)
    practice_hours = models.IntegerField(db_column='uygulamaDersSaati', null=True, blank=True)
    max_students = models.IntegerField(db_column='maxOgrenciSayisi', null=True, blank=True)
    code = models.CharField(max_length=255, db_column='dersKodu', null=True, blank=True)
    name = models.CharField(max_length=255, db_column='dersAdi', null=True, blank=True)
    type = models.ForeignKey(to=CourseType, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True, db_column='courseType_id')
    theory_room_type = models.ForeignKey(to=RoomType, related_name='theory_courses', on_delete=models.SET_NULL, null=True, blank=True, db_column='teorikRoomType_id')
    practice_room_type = models.ForeignKey(to=RoomType, related_name='practice_courses',on_delete=models.SET_NULL, null=True, blank=True, db_column='uygulamaRoomType_id')
    credits = models.IntegerField(db_column='kredi', null=True, blank=True)
    # TODO EDIT
    etkin = models.IntegerField(db_column='etkin', null=True, blank=True)
    sube = models.IntegerField(db_column='sube', null=True, blank=True)
    unpositioned_theory_hours = models.IntegerField(db_column='unpositionedTeorikHours', null=True, blank=True)
    unpositioned_practice_hours = models.IntegerField(db_column='unpositionedUygulamaHours', null=True, blank=True)
    semester = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def full_name(self):
        if self.name == 'reserved':
            return 'reserved'
        return f'{self.code} {self.name}'

    class Meta:
        db_table = 'course'


class CourseVsRoom(models.Model):
    course = models.ForeignKey(to=Course, related_name='rooms', on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to=User, related_name='course_vs_rooms', on_delete=models.SET_NULL, null=True, blank=True)
    lesson_type = models.IntegerField(db_column='lessonType', null=True, blank=True)

    def __str__(self):
        if self.classroom:
            return f'{self.course.name} -> {self.classroom.name}'
        else:
            return self.course.name
    class Meta:
        db_table = 'course_vs_room'


class GradeYear(models.Model):
    department = models.ForeignKey(to=Department, related_name='grade_years', on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.department.name} -> {self.grade}'
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
    old_time = models.IntegerField(db_column='oldtime', null=True)
    new_time = models.IntegerField(db_column='new_time', null=True)
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'editor'


class TimeDay(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column='idtimeDay')
    order_position = models.IntegerField(db_column='orderPosition', null=True, blank=True)
    label = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'timeDay'


class TimeHour(models.Model):
    order_position = models.IntegerField(db_column='orderPosition', null=True, blank=True)
    label = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'timeHour'


class TimeTable(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    time_day = models.ForeignKey(to=TimeDay, on_delete=models.SET_NULL, null=True, blank=True)
    time_hour = models.ForeignKey(to=TimeHour, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField(db_column='yil', null=True)
    semester = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'timeTable'
