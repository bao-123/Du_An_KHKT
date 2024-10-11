# Generated by Django 5.1 on 2024-10-08 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0016_remove_class_form_teacher_remove_class_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='role',
        ),
        migrations.AddField(
            model_name='studentyearprofile',
            name='role',
            field=models.CharField(choices=[('monitor', 'Lớp trưởng'), ('academic', 'lớp phó học tập'), ('art', 'lớp phó văn thể mỹ'), ('labor', 'lớp phó lao động'), ('student', 'Học sinh')], default='student', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentyearprofile',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Du_An.class'),
        ),
    ]