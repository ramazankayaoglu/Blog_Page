# Generated by Django 2.2 on 2019-09-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190911_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=10, verbose_name='Kategori İsim')),
            ],
            options={
                'verbose_name_plural': 'Kategoriler',
            },
        ),
    ]
