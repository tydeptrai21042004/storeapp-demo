from stores.models import *
from rest_framework import serializers


from rest_framework import serializers
from stores.models import NguoiDung
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your actual user model
        fields = ['username', 'email', 'vai_tro']

class NguoiDungSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model  = NguoiDung
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'gioi_tinh', 'avatar', 'vai_tro']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = NguoiDung(**data)
        user.set_password(data['password'])
        user.save()

        return user

    def get_avatar(self, user):
        if user.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % user.avatar.name)
            return '/static/%s' % user.avatar.name



class CuaHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuaHang
        fields = '__all__'

class DanhMucSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMuc
        fields = '__all__'

class SanPhamSerializer(serializers.ModelSerializer):
    anh_san_pham = serializers.SerializerMethodField(source='anh_san_pham')
    danh_muc = serializers.PrimaryKeyRelatedField(queryset=DanhMuc.objects.all())  # Cho phép chọn danh mục từ danh sách có sẵn

    def get_anh_san_pham(self, pro):
        if pro.anh_san_pham:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % pro.anh_san_pham.name)
            return '/static/%s' % pro.anh_san_pham.name

    class Meta:
        model = SanPham
        fields = '__all__'

class GioHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = GioHang
        fields = '__all__'

class SanPhamGioHangSerializer(serializers.ModelSerializer):
    san_pham = SanPhamSerializer() # Hiển thị chi tiết sản phẩm trong giỏ hàng

    class Meta:
        model = SanPhamGioHang
        fields = '__all__'

class DonHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonHang
        fields = '__all__'

class SanPhamDonHangSerializer(serializers.ModelSerializer):
    san_pham = SanPhamSerializer() # Hiển thị chi tiết sản phẩm trong đơn hàng

    class Meta:
        model = SanPhamDonHang
        fields = '__all__'

class DanhGiaSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaSanPham
        fields = '__all__'

class DanhGiaNguoiBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaNguoiBan
        fields = '__all__'

class TinNhanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinNhan
        fields = '__all__'

class ThongKeDoanhThuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThongKeDoanhThu
        fields = '__all__'

class ThongKeDonHangVaSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThongKeDonHangVaSanPhamCuaHang
        fields = '__all__' 
        
        
from rest_framework import serializers
from stores.models import YeuCauXacMinh

class YeuCauXacMinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = YeuCauXacMinh
        fields = '__all__'
from rest_framework import serializers
from stores.models import ThanhToan

class ThanhToanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanhToan
        fields = '__all__'
from rest_framework import serializers
from stores.models import SoSanhSanPham

class SoSanhSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoSanhSanPham
        fields = '__all__'
from rest_framework import serializers
from stores.models import KhoHang

class KhoHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhoHang
        fields = '__all__'
from rest_framework import serializers
from stores.models import NguoiDung
from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # avatar = serializers.FileField(required=True)

    class Meta:
        model = NguoiDung
        fields = ('username', 'email', 'password', 
                #   'avatar', 
                  'vai_tro')

    def create(self, validated_data):
        # avatar = validated_data.pop('avatar')
        # upload_result = cloudinary.uploader.upload(avatar)
        # 🛠 Lưu user + URL ảnh vào database
        user = NguoiDung.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            vai_tro=validated_data['vai_tro'],
            # avatar=upload_result['secure_url']  # 🛠 Lưu URL ảnh
        )
        return user
    
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonHang  # Ensure DonHang model exists
        fields = '__all__'
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaSanPham
        fields = '__all__'
# stores/serializers.py

from rest_framework import serializers
from stores.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username")
    receiver = serializers.CharField(source="receiver.username")

    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "receiver", "message", "created_at"]
