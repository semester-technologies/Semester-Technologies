# Generated by Django 5.2 on 2025-04-18 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_alter_course_course_outline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_outline',
            field=models.TextField(default='Course outline coming soon.', help_text='Detailed breakdown of what the course covers.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='hour_commitment',
            field=models.IntegerField(default=40, help_text='Estimated total hours required to complete the course.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='program_requirements',
            field=models.TextField(default='No special requirements.', help_text='Requirements to enroll for the course (skills, prior knowledge, etc.).'),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateField(default=datetime.date.today, help_text='Course official start date.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='why_take_this_course',
            field=models.TextField(default='Details coming soon.', help_text='Persuasive reasons why someone should take this course.'),
        ),
    ]
