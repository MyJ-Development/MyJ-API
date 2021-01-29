# Generated by Django 2.2.1 on 2021-01-27 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20210127_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estadocliente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ClientStatus'),
        ),
        migrations.AlterField(
            model_name='order',
            name='mediodepago',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.MedioDePago'),
        ),
        migrations.AlterField(
            model_name='order',
            name='prioridad',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Prioridad'),
        ),
    ]