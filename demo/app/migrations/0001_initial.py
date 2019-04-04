# Generated by Django 2.2 on 2019-04-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Article title')),
                ('body', models.TextField(max_length=400, verbose_name='Article body text')),
                ('pub_on', models.DateTimeField(verbose_name='Date this article was published')),
                ('pub_by', models.CharField(max_length=40, verbose_name='Writer that wrote this article')),
                ('wiki_id', models.IntegerField(null=True)),
            ],
        ),
    ]
