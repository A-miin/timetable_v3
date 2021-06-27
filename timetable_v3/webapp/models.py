from django.contrib.auth.models import User, AbstractUser
from django.db import models, transaction
from django.db.models import Subquery, F
from model_clone import CloneMixin
from auditlog.registry import auditlog

SUBE_TYPE = [
    (0, 'bölunmeyecek/birleştirilmeyecek'),
    (1, 'bütün şübelere aynı hoca ve uygun olan sadece bir lab mevcut'),
    (2, 'şubelere bölünecek, hepsine aynı hoca ama birden fazla lab mevcut'),
    (3, 'şuberele bölünecek, her şübeye ayrı hoca ama uygun olan bir lab mevcut'),
    (4, 'şubelere bölünecek, her şübeye ayrı hoca ve ayrı lab mevcut'),
    (5, 'başka bölümün dersi ile birleşik verilecek (teori ve ugulama)'),
    (6, 'başka bölümün dersi ile birleşik verilecek (teori)')
]
LESSON_TYPES = [
    (0, 'Teorik'),
    (1, 'Uygulama')
]
TIMETABLE_RESERVED = 'reserved'


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

    def __str__(self):
        return f'{self.user} -> {self.faculty.name}'


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


class Teacher(CloneMixin, models.Model):
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

    @transaction.atomic
    def create_reserved(self, day_id, hour_id):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=self)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        TimeTable.objects.get_or_create(time_day_id=day_id, time_hour_id=hour_id, classroom=reserved_classroom,
                                        course=reserved_course)

    @transaction.atomic
    def delete_reserved(self, day_id, hour_id):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=self)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        TimeTable.objects.filter(time_day=day_id, time_hour_id=hour_id, classroom=reserved_classroom,
                                 course=reserved_course).delete()

    def list_reserved(self):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=self)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        reserved_timetable = TimeTable.objects.filter(course=reserved_course, classroom=reserved_classroom).\
            order_by('time_day_id', 'time_hour_id')
        result_timetable = [ReservedTimeTable(day=day, hour=hour, reserved=False) for hour in
                            TimeHour.objects.all().order_by('id') for day in
                            TimeDay.objects.all().order_by('id')]
        if reserved_timetable:
            for timetable in result_timetable:
                for reserved in reserved_timetable:
                    if timetable.day == reserved.time_day and timetable.hour == reserved.time_hour:
                        timetable.reserved = True
                        break
        return result_timetable

    class Meta:
        db_table = 'teacher'


class ReservedTimeTable:
    def __init__(self, day, hour, reserved):
        self.day = day
        self.hour = hour
        self.reserved = reserved


class ClassRoom(CloneMixin, models.Model):
    building = models.ForeignKey(to=Building, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True)
    name= models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    room_type = models.ForeignKey(to=RoomType, on_delete=models.SET_NULL, related_name='classrooms', null=True, blank=True, db_column='roomType_id')
    def __str__(self):
        if self.building:
            return f'{self.building.short_name}-{self.name} kapasitesi: {self.capacity}'
        return TIMETABLE_RESERVED

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

    @transaction.atomic
    def create_reserved(self, day_id, hour_id):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=None)[0]
        TimeTable.objects.get_or_create(time_day_id=day_id, time_hour_id=hour_id, classroom=self, course=reserved_course)


    @transaction.atomic
    def delete_reserved(self, day_id, hour_id):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=None)[0]
        TimeTable.objects.filter(time_day=day_id, time_hour_id=hour_id, classroom=self, course=reserved_course).delete()

    def list_reserved(self):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=None)[0]
        reserved_timetable = self.timetable_set.filter(course=reserved_course).order_by('time_day_id', 'time_hour_id')
        result_timetable = [ReservedTimeTable(day=day, hour=hour, reserved=False)  for hour in
                                   TimeHour.objects.all().order_by('id') for day in
                                   TimeDay.objects.all().order_by('id')]
        if reserved_timetable:
            for timetable in result_timetable:
                for reserved in reserved_timetable:
                    if timetable.day == reserved.time_day and timetable.hour == reserved.time_hour:
                        timetable.reserved = True
                        break
        return result_timetable

    def timetable_reserved(self):
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=None)[0]
        reserved_timetable = TimeTable.objects.filter(course=reserved_course, classroom=self)
        return [TimeTable.get_time_hour_day(day=table.time_day, hour=table.time_hour) for table in reserved_timetable]


    class Meta:
        db_table = 'classroom'


class CourseType(models.Model):
    type = models.CharField(max_length=255, null=True)
    type_code = models.IntegerField(db_column='typeCode', null=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'course_type'


class Course(CloneMixin, models.Model):
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
    # year = models.ForeignKey(to='webapp.GradeYear', related_name='courses', on_delete=models.CASCADE)

    def get_reserved_list(self):
        if hasattr(self, 'timetable_reserved_list'):
            return self.timetable_reserved_list
        reserved_grade_year_timetable = [TimeTable.get_time_hour_day(day=table.time_day, hour=table.time_hour)
                                     for table in TimeTable.objects.select_related('time_day', 'time_hour').annotate(reserved_grade_year_course=Subquery(Course.objects.filter(name=TIMETABLE_RESERVED, teacher__name=TIMETABLE_RESERVED, department=self.department, year=self.year).values('id')[:1])).annotate(reserved_classroom=ClassRoom.objects.filter(name=TIMETABLE_RESERVED).values('id')[:1]).
                                         filter(course_id=F('reserved_grade_year_course'), classroom_id=F('reserved_classroom'))]


        reserved_teacher_timetable =  [TimeTable.get_time_hour_day(day=table.time_day, hour=table.time_hour)
     for table in TimeTable.objects.select_related('time_day', 'time_hour').annotate(reserved_teacher_course=Subquery(Course.objects.filter(name=TIMETABLE_RESERVED, teacher=self.teacher).values('id')[:1])).annotate(reserved_classroom=ClassRoom.objects.filter(name=TIMETABLE_RESERVED).values('id')[:1]).
                                             filter(course_id=F('reserved_teacher_course'), classroom_id=F('reserved_classroom'))]
        ids = list(set((reserved_grade_year_timetable + reserved_teacher_timetable)))
        import json
        return json.dumps(ids)

    def set_reserved_list(self, timetable_list):
        l = []
        for table in timetable_list:
            if table.course.teacher == self.teacher or table.course.department == self.teacher and table.course.year == self.year:
                l.append(TimeTable.get_time_hour_day(table.time_day, table.time_hour))
        setattr(self, 'timetable_reserved_list', l)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return TIMETABLE_RESERVED

    def full_name(self):
        if self.name == 'reserved':
            return 'reserved'
        return f'{self.code} {self.name}'

    @property
    def sube_type(self):
        return SUBE_TYPE[self.sube][1]

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

    @property
    def str_lesson_type(self):
        return LESSON_TYPES[self.lesson_type][1]
    class Meta:
        db_table = 'course_vs_room'


class GradeYear(models.Model):
    department = models.ForeignKey(to=Department, related_name='grade_years', on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.department.name} -> {self.grade}'

    @transaction.atomic
    def create_reserved(self, day_id, hour_id):
        reserved_teacher = Teacher.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=reserved_teacher,
                                                       department=self.department, year=self.grade)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        TimeTable.objects.get_or_create(time_day_id=day_id, time_hour_id=hour_id, classroom=reserved_classroom,
                                        course=reserved_course)

    @transaction.atomic
    def delete_reserved(self, day_id, hour_id):
        reserved_teacher = Teacher.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=reserved_teacher,
                                                       department=self.department, year=self.grade)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        TimeTable.objects.filter(time_day=day_id, time_hour_id=hour_id, classroom=reserved_classroom,
                                 course=reserved_course).delete()

    def list_reserved(self):
        reserved_teacher = Teacher.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        reserved_course = Course.objects.get_or_create(name=TIMETABLE_RESERVED, teacher=reserved_teacher,
                                                       department=self.department, year=self.grade)[0]
        reserved_classroom = ClassRoom.objects.get_or_create(name=TIMETABLE_RESERVED)[0]
        reserved_timetable = TimeTable.objects.filter(course=reserved_course, classroom=reserved_classroom). \
            order_by('time_day_id', 'time_hour_id')
        result_timetable = [ReservedTimeTable(day=day, hour=hour, reserved=False) for hour in
                            TimeHour.objects.all().order_by('id') for day in
                            TimeDay.objects.all().order_by('id')]
        if reserved_timetable:
            for timetable in result_timetable:
                for reserved in reserved_timetable:
                    if timetable.day == reserved.time_day and timetable.hour == reserved.time_hour:
                        timetable.reserved = True
                        break
        return result_timetable


    class Meta:
        db_table = 'grade_year'


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


class TimeTable(CloneMixin, models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(to=ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    time_day = models.ForeignKey(to=TimeDay, on_delete=models.SET_NULL, null=True, blank=True)
    time_hour = models.ForeignKey(to=TimeHour, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField(db_column='yil', null=True)
    semester = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'timeTable'

    def __str__(self):
        return f'{self.course.code}->{self.classroom.name}({self.time_day}:{self.time_hour})'

    @staticmethod
    def get_time_day_objects(time_hour_day):
        day, hour = time_hour_day % 5, time_hour_day // 5
        day += 1
        hour += 1
        day = TimeDay.objects.get(id=day)
        hour = TimeHour.objects.get(id=hour)
        return day, hour

    @staticmethod
    def get_time_hour_day(day, hour):
        day, hour = day.id-1, hour.id - 1
        time_hour_day = day + (5 * hour)
        return time_hour_day



auditlog.register(Building)
auditlog.register(Faculty)
auditlog.register(UserFaculty)
auditlog.register(Department)
auditlog.register(RoomType)
auditlog.register(Teacher)
auditlog.register(ClassRoom)
auditlog.register(CourseType)
auditlog.register(CourseVsRoom)
auditlog.register(GradeYear)
auditlog.register(TimeDay)
auditlog.register(TimeHour)
auditlog.register(TimeTable)
