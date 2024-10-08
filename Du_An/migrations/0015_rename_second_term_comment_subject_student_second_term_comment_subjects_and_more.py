# Generated by Django 5.1 on 2024-10-07 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Du_An', '0014_parent_contact_information'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='second_term_comment_subject',
            new_name='second_term_comment_subjects',
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_cuoi_ki',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_giua_ki',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_thuong_xuyen1',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_thuong_xuyen2',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_thuong_xuyen3',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='diem_thuong_xuyen4',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='secondsubject',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='secondsubject',
            name='diem_cuoi_ki',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='secondsubject',
            name='diem_giua_ki',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='secondsubject',
            name='diem_thuong_xuyen1',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='secondsubject',
            name='diem_thuong_xuyen2',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
