# Generated by Django 3.1.4 on 2021-07-24 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0041_auto_20210724_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boq',
            name='itemno',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='boq',
            name='itemqty',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='boq',
            name='unitcost',
            field=models.FloatField(null=True),
        ),
    ]
