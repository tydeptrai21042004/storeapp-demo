# Generated by Django 5.1.4 on 2025-01-10 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_sanpham_anh_san_pham'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='thongkedoanhthusanphamcuahang',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='thongketongsanphamcuahang',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='cua_hang',
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='nam',
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='san_pham',
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='thang',
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='tong_doanh_thu',
        ),
        migrations.RemoveField(
            model_name='thongkedoanhthusanphamcuahang',
            name='tong_san_pham_ban',
        ),
        migrations.RemoveField(
            model_name='thongketongsanphamcuahang',
            name='cua_hang',
        ),
        migrations.RemoveField(
            model_name='thongketongsanphamcuahang',
            name='nam',
        ),
        migrations.RemoveField(
            model_name='thongketongsanphamcuahang',
            name='thang',
        ),
        migrations.RemoveField(
            model_name='thongketongsanphamcuahang',
            name='tong_san_pham',
        ),
    ]
