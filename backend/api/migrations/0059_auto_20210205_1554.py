# Generated by Django 2.2.1 on 2021-02-05 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_auto_20210205_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estadocliente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ClientStatus'),
        ),
        migrations.RemoveField(
            model_name='technician',
            name='type_orders',
        ),
        migrations.AddField(
            model_name='technician',
            name='type_orders',
            field=models.ManyToManyField(to='api.OrderType'),
        ),
    ]
