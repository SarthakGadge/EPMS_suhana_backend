# Generated by Django 4.1.7 on 2024-11-15 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminfeedbackemployee',
            name='direct_report_feedback',
        ),
        migrations.RemoveField(
            model_name='adminfeedbackemployee',
            name='overall_review',
        ),
        migrations.RemoveField(
            model_name='adminfeedbackmanager',
            name='direct_report_feedback',
        ),
        migrations.RemoveField(
            model_name='adminfeedbackmanager',
            name='overall_review',
        ),
    ]
