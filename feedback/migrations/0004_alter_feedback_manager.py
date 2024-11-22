# Generated by Django 4.1.7 on 2024-11-22 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
        ('feedback', '0003_remove_feedback_from_user_remove_feedback_to_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.manager'),
        ),
    ]
