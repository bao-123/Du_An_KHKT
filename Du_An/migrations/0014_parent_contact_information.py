# Generated by Django 5.1 on 2024-10-01 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0013_secondsubject_name_alter_student_comment_subjects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='contact_information',
            field=models.TextField(default=''),
        ),
    ]
