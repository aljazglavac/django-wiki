# Generated by Django 2.2 on 2019-04-13 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oseba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wiki_id', models.IntegerField(null=True)),
                ('ime', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Knjiga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wiki_id', models.IntegerField(null=True)),
                ('naslov', models.CharField(max_length=100)),
                ('oseba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app5.Oseba')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]