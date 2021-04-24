from django import forms

from webapp.models import ClassRoom, Building, Department, RoomType
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
