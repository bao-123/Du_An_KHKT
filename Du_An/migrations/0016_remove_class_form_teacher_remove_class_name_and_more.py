# Generated by Django 5.1 on 2024-10-08 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0015_rename_second_term_comment_subject_student_second_term_comment_subjects_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='form_teacher',
        ),
        migrations.RemoveField(
            model_name='class',
            name='name',
        ),
        migrations.RemoveField(
            model_name='class',
            name='subject_teachers',
        ),
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.RemoveField(
            model_name='student',
            name='comment_subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='main_subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='second_subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='second_term_comment_subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='second_term_main_subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='second_term_second_subjects',
        ),
        migrations.AlterField(
            model_name='evaluatebycommentsubject',
            name='is_passed',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.CreateModel(
            name='ClassYearProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=2024)),
                ('name', models.CharField(max_length=3, unique=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='Du_An.class')),
                ('form_teacher', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_class', to='Du_An.teacher')),
                ('subject_teachers', models.ManyToManyField(related_name='classroom', to='Du_An.classsubjectteacher')),
            ],
        ),
        migrations.CreateModel(
            name='StudentYearProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=2024)),
                ('classroom', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Du_An.class')),
                ('comment_subjects', models.ManyToManyField(related_name='student', to='Du_An.evaluatebycommentsubject')),
                ('main_subjects', models.ManyToManyField(related_name='student', to='Du_An.mainsubject')),
                ('second_subjects', models.ManyToManyField(related_name='student', to='Du_An.secondsubject')),
                ('second_term_comment_subjects', models.ManyToManyField(related_name='second_term_student', to='Du_An.evaluatebycommentsubject')),
                ('second_term_main_subjects', models.ManyToManyField(related_name='second_term_student', to='Du_An.mainsubject')),
                ('second_term_second_subjects', models.ManyToManyField(related_name='second_term_student', to='Du_An.secondsubject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='Du_An.student')),
            ],
        ),
    ]
