# Generated by Django 2.2 on 2019-09-14 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(related_name='blog', to='blog.Kategori'),
        ),
    ]
