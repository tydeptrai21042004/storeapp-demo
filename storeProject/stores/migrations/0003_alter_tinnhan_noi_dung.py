# Generated by Django 5.1.4 on 2025-01-10 07:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_alter_nguoidung_anh_dai_dien_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinnhan',
            name='noi_dung',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
