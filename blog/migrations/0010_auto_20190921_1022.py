# Generated by Django 2.2 on 2019-09-21 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190920_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='Default/hqdefault.jpg', help_text='Kapak Fotoğrafı yükleyiniz.', null=True, upload_to='blog', verbose_name='Resim'),
        ),
    ]
