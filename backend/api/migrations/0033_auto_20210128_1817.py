# Generated by Django 2.2.1 on 2021-01-28 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20210128_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estadocliente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ClientStatus'),
        ),
    ]