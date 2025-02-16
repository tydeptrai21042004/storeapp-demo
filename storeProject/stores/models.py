from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Vai tro nguoi dung
class NguoiDung(AbstractUser):
    VAI_TRO = [
        ('user', 'Nguoi dung thuong'),
        ('seller', 'Nguoi ban'),
        ('admin', 'Quan tri vien'),
        ('staff', 'Nhan vien he thong'),
    ]
    GIOI_TINH = [
        ('male', 'Nam'),
        ('female', 'Nu'),
        ('other', 'Khac'),
    ]

    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=200, blank=True, default='https://console.aiven.io/static/images/service-onboarding-banner.4d81fe52.png')
    vai_tro = models.CharField(max_length=20, choices=VAI_TRO, default='user')
    gioi_tinh = models.CharField(max_length=10, choices=GIOI_TINH, blank=True, null=True)
    da_xac_minh = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.get_vai_tro_display()})"


class DonHang(models.Model):
    TRANG_THAI_CHOICES = [
        ("pending", "Đang xử lý"),
        ("shipped", "Đã gửi hàng"),
        ("delivered", "Đã giao"),
        ("canceled", "Đã hủy"),
    ]
    
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name="don_hang")
    ngay_tao = models.DateTimeField(auto_now_add=True)
    phuong_thuc_thanh_toan = models.CharField(max_length=20, choices=[
        ("cod", "Thanh toán khi nhận hàng"), 
        ("paypal", "PayPal"), 
        ("stripe", "Stripe"), 
        ("zalo", "Zalo Pay"), 
        ("momo", "MoMo")
    ])
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    da_thanh_toan = models.BooleanField(default=False)
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES, default="pending")  # New field

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.trang_thai}"
# Cua hang
class CuaHang(models.Model):
    chu_so_huu = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='cua_hang')  # Chu so huu
    ten = models.CharField(max_length=100)  # Ten cua hang
    mo_ta = RichTextField(blank=True, null=True)  # Mo ta cua hang
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Thoi gian tao
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ten

    class Meta:
        unique_together = ('chu_so_huu',)


# Danh muc san pham
class DanhMuc(models.Model):
    ten = models.CharField(max_length=100)  # Ten danh muc
    mo_ta = RichTextField(blank=True, null=True)  # Mo ta danh muc

    def __str__(self):
        return self.ten


# San pham
class SanPham(models.Model):
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='san_pham')  # Cửa hàng
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.SET_NULL, null=True, related_name='san_pham')  # Danh mục
    ten = models.CharField(max_length=100)  # Tên sản phẩm
    mo_ta = RichTextField(blank=True, null=True)  # Mô tả sản phẩm
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    so_luong_ton = models.PositiveIntegerField(default=0)  # Số lượng tồn
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    ngay_cap_nhat = models.DateTimeField(auto_now=True)  # Ngày cập nhật
    anh_san_pham = models.ImageField(upload_to='products/%Y/%m', blank=True, null=True)  # Ảnh sản phẩm
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ten

    class Meta:
        unique_together = ('ten', 'cua_hang')


# Giỏ hàng
class GioHang(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='gio_hang')  # Người dùng
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tổng tiền

    def tinh_tong_tien(self):
        total = sum([sp.gia * sp.so_luong for sp in self.san_pham.all()])
        self.tong_tien = total
        self.save()

    def __str__(self):
        return f"Gio hang của {self.nguoi_dung.username}"

# Sản phẩm trong giỏ hàng
class SanPhamGioHang(models.Model):
    gio_hang = models.ForeignKey(GioHang, on_delete=models.CASCADE, related_name='san_pham')  # Giỏ hàng
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)  # Sản phẩm
    so_luong = models.PositiveIntegerField()  # Số lượng
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá

    def __str__(self):
        return f"{self.so_luong} x {self.san_pham.ten} trong giỏ hàng của {self.gio_hang.nguoi_dung.username}"

    class Meta:
        unique_together = ('gio_hang', 'san_pham')





# San pham trong don hang
class SanPhamDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name='san_pham')  # Don hang
    san_pham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True)  # San pham
    so_luong = models.PositiveIntegerField()  # So luong
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Gia

    def __str__(self):
        return f"{self.so_luong} x {self.san_pham.ten} (Don hang #{self.don_hang.id})"

    class Meta:
        unique_together = ('don_hang', 'san_pham')


# Danh gia san pham
class DanhGiaSanPham(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name='danh_gia')  # San pham
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='danh_gia_san_pham')  # Nguoi dung
    diem = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Diem danh gia
    binh_luan = models.TextField(blank=True, null=True)  # Binh luan
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngay tao

    def __str__(self):
        return f"Danh gia cho {self.san_pham.ten} boi {self.nguoi_dung.username}"

    class Meta:
        unique_together = ('san_pham', 'nguoi_dung')


# Danh gia nguoi ban
class DanhGiaNguoiBan(models.Model):
    nguoi_ban = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='danh_gia_nguoi_ban')  # Nguoi ban
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='danh_gia_nguoi_ban')  # Nguoi dung
    diem = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Diem danh gia
    binh_luan = models.TextField(blank=True, null=True)  # Binh luan
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Ngay tao

    def __str__(self):
        return f"Danh gia cho {self.nguoi_ban.ten} boi {self.nguoi_dung.username}"

    class Meta:
        unique_together = ('nguoi_ban', 'nguoi_dung')


# Tin nhan chat (tich hop Firebase)
class TinNhan(models.Model):
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan_gui')  # Nguoi gui
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan_nhan')  # Nguoi nhan
    noi_dung = RichTextField()  # Noi dung tin nhan
    thoi_gian = models.DateTimeField(auto_now_add=True)  # Thoi gian gui

    def __str__(self):
        return f"Tin nhan tu {self.nguoi_gui.username} den {self.nguoi_nhan.username}"


class ThongKeDoanhThu(models.Model):
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name='thong_ke_doanh_thu')
    so_luong = models.PositiveIntegerField(default=0)
    gia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ngay_thanh_toan = models.DateTimeField()
    tong_doanh_thu = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Doanh thu từ {self.san_pham.ten} - {self.cua_hang.ten} vào {self.ngay_thanh_toan.strftime('%d/%m/%Y')}"


class ThongKeDonHangVaSanPhamCuaHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE)  # Đơn hàng
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)  # Sản phẩm
    cua_hang = models.ForeignKey(CuaHang, on_delete=models.CASCADE)  # Cửa hàng
    so_luong = models.PositiveIntegerField()  # Số lượng sản phẩm đã bán
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá của sản phẩm
    ngay_dat_hang = models.DateTimeField()  # Ngày đặt hàng

    def __str__(self):
        return f"Thống kê cho {self.san_pham.ten} trong đơn hàng #{self.don_hang.id}"


class YeuCauXacMinh(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name="yeu_cau_xac_minh")
    trang_thai = models.CharField(max_length=10, choices=[("pending", "Pending"), ("approved", "Approved")], default="pending")
    ngay_gui = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Xác minh {self.nguoi_dung.username} - {self.trang_thai}"
class ThanhToan(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name="thanh_toan")
    phuong_thuc = models.CharField(max_length=20, choices=[
        ("paypal", "PayPal"),
        ("stripe", "Stripe"),
        ("zalo", "Zalo Pay"),
        ("momo", "MoMo"),
    ])
    ma_giao_dich = models.CharField(max_length=100, unique=True)  # Transaction ID
    trang_thai = models.CharField(max_length=10, choices=[
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ])
    ngay_thanh_toan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thanh toán {self.don_hang.id} ({self.phuong_thuc})"

class SoSanhSanPham(models.Model):
    san_pham_goc = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name="so_sanh_goc")
    san_pham_so_sanh = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name="so_sanh_tuong_tu")
    diem_tuong_dong = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])  # Similarity score (0-1)

    def __str__(self):
        return f"So sánh {self.san_pham_goc.ten} với {self.san_pham_so_sanh.ten}"
class KhoHang(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name="kho_hang")
    so_luong_nhap = models.PositiveIntegerField()  # Quantity added
    ngay_nhap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.so_luong_nhap} sản phẩm {self.san_pham.ten} đã nhập vào kho"

# stores/models.py

from djongo import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.message[:20]}..."
