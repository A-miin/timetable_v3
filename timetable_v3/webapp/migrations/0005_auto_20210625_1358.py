# Generated by Django 3.1.7 on 2021-06-25 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20210507_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetablegenerator',
            name='course',
        ),
        migrations.RemoveField(
            model_name='timetablegenerator',
            name='department',
        ),
        migrations.RemoveField(
            model_name='timetablegenerator',
            name='grade_year',
        ),
        migrations.RemoveField(
            model_name='timetablegenerator',
            name='room',
        ),
        migrations.RemoveField(
            model_name='timetablegenerator',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Editor',
        ),
        migrations.DeleteModel(
            name='TimeTableGenerator',
        ),
    ]
