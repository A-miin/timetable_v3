from django import forms

from webapp.models import ClassRoom, Building, Department, RoomType, Teacher, GradeYear, Course, CourseVsRoom, \
    CourseType, SUBE_TYPE
from django.contrib.auth.models import User


class ClassRoomForm(forms.ModelForm):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), label='Bina')
    name = forms.CharField(label='Ders Oda Adı')
    capacity = forms.CharField(label='Kapasite')
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), label='Derslik Türü')

    def __init__(self, user, *args, **kwargs):
        super(ClassRoomForm, self).__init__(*args, **kwargs)
        self.fields['department'] = forms.ModelChoiceField(
            queryset=Department.objects.filter(faculty=user.faculty.faculty),
        label='Bölüm')
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'hideable'}))
        self.fields['user'].initial = user.id

    class Meta:
        model = ClassRoom
        fields = ('building',
                  'department',
                  'name',
                  'capacity',
                  'room_type',
                  'user')


EMPLOYEE_TYPE = [
    (0, 'Tam Zamanlı'),
    (1, 'Yarı Zamanlı'),
    (2, 'DSU')
]


class TeacherForm(forms.ModelForm):
    code = forms.IntegerField(label='Sicil')
    name = forms.CharField(label='Name')
    unvan = forms.CharField(label='Unvan')
    employee_type = forms.ChoiceField(choices=EMPLOYEE_TYPE)

    def __init__(self, user, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'hideable'}))
        self.fields['user'].initial = user.id

    class Meta:
        model = Teacher
        fields = ('code',
                  'name',
                  'unvan',
                  'employee_type',
                  'user')


class GradeYearForm(forms.ModelForm):
    grade = forms.IntegerField(label='Sınıf')

    def __init__(self, user, *args, **kwargs):
        super(GradeYearForm, self).__init__(*args, **kwargs)
        self.fields['department'] = forms.ModelChoiceField(
            queryset=Department.objects.filter(faculty=user.faculty.faculty),
            label='Bölüm')

    class Meta:
        model = GradeYear
        fields = ('department',
                  'grade')

SEMESTER_TYPES = [
    ('Güz', 'Güz'),
    ('Bahar', 'Bahar')
]


class CourseForm(forms.ModelForm):
    theory_hours = forms.IntegerField(label='Teorik ders saati')
    practice_hours = forms.IntegerField(label='Uygulama ders saati')
    credits = forms.IntegerField(label='Kredi')
    max_students = forms.IntegerField(label='Max ogrenci sayisi')
    code = forms.CharField(label='Ders kodu')
    name = forms.CharField(label='Ders adi')
    type = forms.ModelChoiceField(queryset=CourseType.objects.all(), label='Ders türü')
    semester = forms.ChoiceField(choices=SEMESTER_TYPES, label='Dönem')
    theory_room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), label='Teorik ders icin derslik tibi')
    practice_room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), label='Uygulama ders icin derslik tibi')
    sube = forms.ChoiceField(choices=SUBE_TYPE, label='Şübelere bölme yada birleştirme modu')
    year = forms.IntegerField(label='Sinif')

    def __init__(self, user, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['department'] = forms.ModelChoiceField(
            queryset=Department.objects.filter(faculty=user.faculty.faculty),
            label='Bölüm')
        self.fields['teacher'] = forms.ModelChoiceField(
            queryset=Teacher.objects.filter(user=user), label='Öğretmen'
        )
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(),
                                                     widget=forms.HiddenInput(attrs={'class': 'hideable'}))
        self.fields['user'].initial = user.id

    class Meta:
        model = Course
        fields = ('department',
                  'teacher',
                  'theory_hours',
                  'practice_hours',
                  'max_students',
                  'code',
                  'name',
                  'type',
                  'theory_room_type',
                  'practice_room_type',
                  'credits',
                  'etkin',
                  'sube',
                  'semester',
                  'year',
                  'user')


COURSE_VS_ROOM_TYPES = [
    (0, 'Teorik'),
    (1, 'Uygulama')
]

class CourseVsRoomForm(forms.ModelForm):
    lesson_type = forms.ChoiceField(choices=COURSE_VS_ROOM_TYPES)

    def __init__(self, user, *args, **kwargs):
        super(CourseVsRoomForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(),
                                                     widget=forms.HiddenInput(attrs={'class': 'hideable'}))
        self.fields['user'].initial = user.id
        self.fields['course'] = forms.ModelChoiceField(queryset=Course.objects.filter(user=user),
                                                       label='Ders')
        self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.select_related('building').
                                                          filter(user=user), label='Derslik')


    class Meta:
        model = CourseVsRoom
        fields = ('course',
                  'classroom',
                  'lesson_type',
                  'user')