# Generated by Django 3.1.4 on 2021-03-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0003_auto_20210225_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='approved_boq',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='submitted_boq',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='temp_projects',
            name='submitted_boq',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='temp_projects',
            name='schedule',
            field=models.IntegerField(),
        ),
    ]
