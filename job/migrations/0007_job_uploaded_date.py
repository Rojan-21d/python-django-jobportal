# Generated by Django 5.1.2 on 2024-10-18 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_category_alter_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='uploaded_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
