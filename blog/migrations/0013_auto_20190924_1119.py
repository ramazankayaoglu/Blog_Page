# Generated by Django 2.2 on 2019-09-24 08:19

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190921_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(max_length=5000, null=True, verbose_name='içerik'),
        ),
    ]
