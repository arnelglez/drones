# Generated by Django 4.0.7 on 2022-08-07 01:23

import api.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=100, unique=True, validators=[api.validators.serial_drone])),
                ('model', models.IntegerField(choices=[(0, 'Lightweight'), (1, 'Middleweight'), (2, 'Cruiserweight'), (3, 'Heavyweight')], default=0)),
                ('weight', models.FloatField(max_length=5, validators=[api.validators.weight_drone])),
                ('battery', models.FloatField(validators=[api.validators.batery_drone])),
                ('state', models.IntegerField(choices=[(0, 'IDLE'), (1, 'LOADING'), (2, 'LOADED'), (3, 'DELIVERING'), (4, 'DELIVERED'), (5, 'RETURNING')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, validators=[api.validators.name_medication])),
                ('weight', models.FloatField()),
                ('code', models.CharField(max_length=150, unique=True, validators=[api.validators.code_medication])),
                ('image', models.ImageField(blank=True, null=True, upload_to='medication/')),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(blank=True, default=1, null=True)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.drone')),
            ],
        ),
        migrations.CreateModel(
            name='TransportationMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('medication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.medication')),
                ('transportation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.transportation')),
            ],
        ),
        migrations.AddField(
            model_name='transportation',
            name='medications',
            field=models.ManyToManyField(related_name='medications', through='api.TransportationMedication', to='api.medication'),
        ),
        migrations.CreateModel(
            name='DroneBatteryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery', models.FloatField(validators=[api.validators.batery_drone])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.drone')),
            ],
        ),
    ]
