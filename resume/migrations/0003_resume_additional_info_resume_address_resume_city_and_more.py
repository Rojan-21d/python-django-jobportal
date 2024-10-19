# Generated by Django 5.1.2 on 2024-10-17 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='additional_info',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='company_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='resume',
            name='course_title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='resume',
            name='date_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='date_to',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='degree_certification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='graduation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='job_position',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='resume',
            name='level',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='resume',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='resume',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='skill_proficiency',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='resume',
            name='skills',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='resume',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='university_college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
