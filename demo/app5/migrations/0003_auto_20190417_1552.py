# Generated by Django 2.2 on 2019-04-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app5', '0002_auto_20190415_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knjiga',
            name='wiki_id',
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='oseba',
            name='wiki_id',
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
    ]