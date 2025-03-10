# Generated by Django 5.1.4 on 2025-01-09 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoidung',
            name='anh_dai_dien',
            field=models.ImageField(blank=True, null=True, upload_to='stores/%Y/%m'),
        ),
        migrations.AlterUniqueTogether(
            name='cuahang',
            unique_together={('chu_so_huu',)},
        ),
        migrations.AlterUniqueTogether(
            name='danhgianguoiban',
            unique_together={('nguoi_ban', 'nguoi_dung')},
        ),
        migrations.AlterUniqueTogether(
            name='danhgiasanpham',
            unique_together={('san_pham', 'nguoi_dung')},
        ),
        migrations.AlterUniqueTogether(
            name='sanpham',
            unique_together={('ten', 'cua_hang')},
        ),
        migrations.AlterUniqueTogether(
            name='sanphamdonhang',
            unique_together={('don_hang', 'san_pham')},
        ),
        migrations.AlterUniqueTogether(
            name='thongkedoanhthu',
            unique_together={('nguoi_ban', 'thang', 'nam')},
        ),
    ]
