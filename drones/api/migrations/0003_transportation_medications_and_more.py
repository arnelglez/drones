# Generated by Django 4.0.7 on 2022-08-04 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_transportation_medications'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportation',
            name='medications',
            field=models.ManyToManyField(related_name='medications', through='api.TransportationMedication', to='api.medication'),
        ),
        migrations.AlterField(
            model_name='transportationmedication',
            name='medication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.medication'),
        ),
        migrations.AlterField(
            model_name='transportationmedication',
            name='transportation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.transportation'),
        ),
    ]
