# Generated by Django 5.1.2 on 2024-10-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='est_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
