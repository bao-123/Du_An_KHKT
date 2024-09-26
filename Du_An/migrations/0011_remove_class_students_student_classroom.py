# Generated by Django 5.1 on 2024-09-25 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0010_student_comment_subjects_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Du_An.class'),
            preserve_default=False,
        ),
    ]