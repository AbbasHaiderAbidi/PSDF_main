# Generated by Django 3.1.4 on 2021-04-01 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0026_auto_20210401_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tesg_master',
            name='admin_req_date',
        ),
    ]
