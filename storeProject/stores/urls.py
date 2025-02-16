from stores import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from stores.views import admin_stats, approve_seller
# Register routers for ViewSets
router = DefaultRouter()
router.register('nguoi-dung', views.NguoiDungViewSet, basename='nguoidung')
router.register('cua-hang', views.CuaHangViewSet, basename='cuahang')
router.register('danh-muc', views.DanhMucViewSet, basename='danhmuc')
router.register('san-pham', views.SanPhamViewSet, basename='sanpham')
router.register('don-hang', views.DonHangViewSet, basename='donhang')
router.register('gio-hang', views.GioHangViewSet, basename='giohang')
router.register('sanpham-giohang', views.SanPhamGioHangViewSet, basename='sanphamgiohang')
router.register('danhgia-sanpham', views.DanhGiaSanPhamViewSet, basename='danhgiasanpham')
router.register('danhgia-nguoiban', views.DanhGiaNguoiBanViewSet, basename='danhgianguoiban')
router.register('sanpham-donhang', views.SanPhamDonHangViewSet, basename='sanphamdonhang')
router.register('tin-nhan', views.TinNhanViewSet, basename='tinnhan')
router.register('thongke-doanhthu', views.ThongKeDoanhThuViewSet, basename='thongkedoanhthu')
router.register('thongke-donhangsanpham', views.ThongKeDonHangVaSanPhamViewSet, basename='thongkedonhangsanpham')

# ✅ New Endpoints
router.register('yeu-cau-xac-minh', views.YeuCauXacMinhViewSet, basename='yeucauxacminh')
router.register('thanh-toan', views.ThanhToanViewSet, basename='thanhtoan')
router.register('so-sanh-san-pham', views.SoSanhSanPhamViewSet, basename='sosanhsanpham')
router.register('kho-hang', views.KhoHangViewSet, basename='khohang')
from stores.views import approve_seller
from stores.views import admin_stats, approve_seller, delete_seller  # ✅ Import delete_seller
# stores/urls.py

from django.urls import path
from stores.views import send_message, get_chat_messages

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', include(router.urls)),
    path('nguoi-dung/<str:username>/approve/', approve_seller, name='approve_seller'),  # ✅ Accept username instead of id
    path('nguoi-dung/<str:username>/delete/', delete_seller, name='delete_seller'),  # ✅ Accept username instead of id
    path('auth/create-staff/', views.AuthViewSet.as_view({'post': 'create_staff'}), name='create_staff'),  # ✅ Add this line

    path('auth/register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),
    path("admin/stats/", admin_stats, name="admin_stats"),
    path("chat/send/", send_message, name="send_message"),
    path("chat/<str:username>/", get_chat_messages, name="get_chat_messages"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)