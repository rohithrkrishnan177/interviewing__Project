# Generated by Django 3.2.11 on 2022-01-15 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interviewer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cantidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.DecimalField(decimal_places=1, max_digits=4)),
                ('address', models.TextField()),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cantidate_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_date', models.DateField(auto_now_add=True, verbose_name='Interview Date')),
                ('queries', models.TextField()),
                ('department', models.CharField(choices=[('TL', 'Team_Lead'), ('SD', 'Senior_Developer'), ('MC', 'Manager')], default='TL', max_length=3)),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Release Date')),
                ('assigned_interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviewer.inter_viewer')),
                ('cantidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cantidate.cantidate')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(verbose_name='Appointment date')),
                ('appointment_time', models.TimeField(verbose_name='Appointement time')),
                ('status', models.BooleanField(default=False)),
                ('cantidate_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cantidate_appointments', to='cantidate.cantidate_history')),
                ('interviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interview_appointments', to='interviewer.inter_viewer')),
            ],
        ),
    ]
