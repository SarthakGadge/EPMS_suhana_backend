# Generated by Django 4.1.7 on 2024-11-06 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_text', models.TextField()),
                ('feedback_type', models.CharField(choices=[('Direct Report', 'Direct Report'), ('Employee to Admin', 'Employee to Admin'), ('Employee to Manager', 'Employee to Manager'), ('Manager to admin', 'Manager to admin'), ('Manager to Employee', 'Manager to Employee')], max_length=20)),
                ('anonymous', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('feedback_status', models.CharField(choices=[('Acknowledged', 'Acknowledged'), ('Pending', 'Pending'), ('Responded', 'Responded')], default='Pending', max_length=20)),
                ('response', models.TextField(blank=True, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_given', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
