# Generated by Django 4.2.7 on 2024-03-28 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=500)),
                ('lastName', models.CharField(max_length=500)),
                ('speciality', models.CharField(max_length=500)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=500)),
                ('lastName', models.CharField(max_length=500)),
                ('address', models.TextField()),
                ('contact', models.IntegerField(null=True)),
                ('dob', models.CharField(default='2023-01-01', max_length=500)),
                ('gender', models.CharField(max_length=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=50)),
                ('height', models.DecimalField(decimal_places=2, max_digits=50)),
                ('healthHistory', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('medication', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('appointment', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leadsstatus', to='healthcare.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leadsstatus', to='healthcare.patient')),
            ],
        ),
    ]
