# Generated by Django 5.1 on 2024-10-22 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0018_remove_classyearprofile_name_class_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classyearprofile',
            name='subject_teachers',
        ),
        migrations.AddField(
            model_name='classsubjectteacher',
            name='classroom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subject_teachers', to='Du_An.classyearprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classyearprofile',
            name='form_teacher',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_class', to='Du_An.teacher'),
        ),
    ]
