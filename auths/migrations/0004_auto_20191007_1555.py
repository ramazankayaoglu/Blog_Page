# Generated by Django 2.2 on 2019-10-07 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_auto_20191002_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[(None, 'Cinsiyet Seçiniz'), ('diger', 'DİĞER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN')], max_length=6, null=True, verbose_name='Cinsiyet'),
        ),
    ]
