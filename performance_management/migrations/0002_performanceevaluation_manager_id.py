# Generated by Django 4.1.7 on 2024-11-07 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
        ('performance_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='performanceevaluation',
            name='manager_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.manager'),
        ),
    ]
