# Generated by Django 2.2.1 on 2021-01-29 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20210129_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estadocliente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ClientStatus'),
        ),
    ]
