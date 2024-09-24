# Generated by Django 5.1 on 2024-09-24 09:56

import Du_An.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0009_evaluatebycommentsubject'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='comment_subjects',
            field=models.ManyToManyField(default=Du_An.models.EvaluateByCommentSubject.generate_comment_subject, related_name='students', to='Du_An.evaluatebycommentsubject'),
        ),
        migrations.AlterField(
            model_name='student',
            name='second_subjects',
            field=models.ManyToManyField(default=Du_An.models.SecondSubject.generate_second_subjects, related_name='student', to='Du_An.secondsubject'),
        ),
    ]
