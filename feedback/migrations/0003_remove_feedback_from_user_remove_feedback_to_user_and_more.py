# Generated by Django 4.1.7 on 2024-11-21 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
        ('feedback', '0002_alter_feedback_anonymous_alter_feedback_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='to_user',
        ),
        migrations.AddField(
            model_name='feedback',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userauth.employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userauth.manager'),
            preserve_default=False,
        ),
    ]
