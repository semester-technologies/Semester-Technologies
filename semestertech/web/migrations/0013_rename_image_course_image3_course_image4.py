# Generated by Django 5.2 on 2025-04-18 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_course_image1_course_image2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='image',
            new_name='image3',
        ),
        migrations.AddField(
            model_name='course',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
    ]
