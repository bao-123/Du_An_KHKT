# Generated by Django 5.1 on 2024-09-21 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0006_secondsubject_student_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='role',
            field=models.CharField(choices=[('monitor', 'Lớp trưởng'), ('academic', 'lớp phó học tập'), ('art', 'lớp phó văn thể mỹ'), ('labor', 'lớp phó lao động'), ('student', 'Học sinh')], max_length=30),
        ),
    ]