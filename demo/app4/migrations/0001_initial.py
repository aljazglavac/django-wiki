# Generated by Django 2.2 on 2019-04-12 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('wikimodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wiki.WikiModel')),
                ('fish_name', models.CharField(max_length=30)),
            ],
            bases=('wiki.wikimodel',),
        ),
    ]
