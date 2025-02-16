from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from stores.models import *
from rest_framework import viewsets, generics, status, parsers, permissions
from stores import serializers, paginators
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from stores.models import NguoiDung, DonHang, DanhGiaSanPham
from stores.serializers import UserSerializer, OrderSerializer, ProductReviewSerializer

class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.filter(is_active=True).all()
    serializer_class = UserSerializer

    # ✅ Get the current logged-in user profile
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # ✅ Update user profile
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        user = self.get_object()
        if user != request.user:
            return Response({"error": "You can only update your own profile"}, status=403)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # ✅ Get a user's order history
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def orders(self, request):
        orders = DonHang.objects.filter(nguoi_dung=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # ✅ Get all reviews by this user
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        reviews = DanhGiaSanPham.objects.filter(nguoi_dung=pk)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)



from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from stores.models import CuaHang
from stores.serializers import CuaHangSerializer

# ViewSet quản lý cửa hàng
class CuaHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CuaHang.objects.filter(active=True).all()  # Chỉ lấy cửa hàng đang hoạt động
    serializer_class = CuaHangSerializer  # Chọn serializer cho cửa hàng

    # API Tạo cửa hàng cho người bán
    @action(methods=['post'], detail=False, url_path='create-store')
    def create_store(self, request):
        user = request.user  # Lấy thông tin người dùng hiện tại

        # Kiểm tra nếu không phải người bán hoặc chưa được xác minh
        if user.vai_tro != 'seller' or not user.da_xac_minh:
            return Response({'detail': 'Bạn không có quyền tạo cửa hàng'}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra nếu người dùng đã có cửa hàng
        if CuaHang.objects.filter(chu_so_huu=user).exists():
            return Response({'detail': 'Bạn đã có cửa hàng'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy thông tin cửa hàng từ request
        store_data = request.data
        store_name = store_data.get('ten')
        store_description = store_data.get('mo_ta')

        # Kiểm tra dữ liệu nhập vào
        if not store_name or not store_description:
            return Response({'detail': 'Tên cửa hàng và mô tả là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo cửa hàng mới
        cua_hang = CuaHang.objects.create(
            chu_so_huu=user,
            ten=store_name,
            mo_ta=store_description
        )

        return Response(CuaHangSerializer(cua_hang).data, status=status.HTTP_201_CREATED)

    # API lấy thông tin cửa hàng của người dùng
    @action(methods=['get'], detail=False, url_path='my-store')
    def my_store(self, request):
        store = CuaHang.objects.filter(chu_so_huu=request.user).first()
        if not store:
            return Response({'detail': 'Bạn chưa có cửa hàng'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CuaHangSerializer(store).data)



# ViewSet quản lý danh mục sản phẩm
class DanhMucViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhMuc.objects.all()  # Lấy tất cả danh mục
    serializer_class = serializers.DanhMucSerializer  # Chọn serializer cho danh mục

    # API lấy sản phẩm trong một danh mục
    @action(methods=['get'], detail=True)
    def sanpham(self, request, pk):
        sanpham = self.get_object().san_pham.all()  # Lấy tất cả sản phẩm trong danh mục

        return Response(serializers.SanPhamSerializer(sanpham, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from stores.models import SanPham, DanhMuc, CuaHang
from stores.serializers import SanPhamSerializer
from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stores.models import SanPham, CuaHang
from stores.serializers import SanPhamSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stores.models import SanPham, CuaHang
from stores.serializers import SanPhamSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # ✅ Require authentication
def my_products(request):
    user = request.user

    # 🚨 Double-check authentication to prevent AnonymousUser errors
    if not user or user.is_anonymous:
        return Response({'detail': 'Người dùng chưa đăng nhập'}, status=401)

    # Find the store owned by the user
    store = CuaHang.objects.filter(chu_so_huu=user).first()

    if not store:
        return Response({'detail': 'Bạn chưa có cửa hàng'}, status=404)

    # Get products belonging to the store
    products = SanPham.objects.filter(cua_hang=store, active=True)
    return Response(SanPhamSerializer(products, many=True).data, status=200)


# ViewSet quản lý sản phẩm
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.parsers import MultiPartParser, FormParser

class SanPhamViewSet(viewsets.ViewSet, generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # ✅ Allow file uploads

    def create(self, request, *args, **kwargs):
        print("🔍 Authenticated User:", request.user)
        print("🔍 Is Authenticated:", request.user.is_authenticated)
        print("🔍 Request Headers:", request.headers.get("Authorization"))
        print("🔍 Request Content-Type:", request.content_type)  # ✅ Debug Content-Type
        print("🔍 Request Data:", request.data)  # ✅ Debug Request Body

        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Bạn phải đăng nhập để tạo sản phẩm'}, status=status.HTTP_401_UNAUTHORIZED)
        if not hasattr(user, 'vai_tro'):
            return Response({'detail': 'Vai trò của bạn không hợp lệ'}, status=status.HTTP_403_FORBIDDEN)

        if user.vai_tro != 'seller':
            return Response({'detail': 'Bạn không có quyền tạo sản phẩm'}, status=status.HTTP_403_FORBIDDEN)

        store = CuaHang.objects.filter(chu_so_huu=user).first()
        if not store:
            return Response({'detail': 'Bạn phải có cửa hàng để tạo sản phẩm'}, status=status.HTTP_400_BAD_REQUEST)

        danh_muc_id = request.data.get('danh_muc')
        try:
            danh_muc = DanhMuc.objects.get(id=danh_muc_id)
        except DanhMuc.DoesNotExist:
            return Response({'detail': 'Danh mục không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Handle file upload properly
        anh_san_pham = request.FILES.get('anh_san_pham')

        san_pham = SanPham.objects.create(
            cua_hang=store,
            danh_muc=danh_muc,
            ten=request.data.get('ten'),
            mo_ta=request.data.get('mo_ta'),
            gia=request.data.get('gia'),
            so_luong_ton=request.data.get('so_luong_ton', 0),
            anh_san_pham=anh_san_pham,
        )

        return Response(SanPhamSerializer(san_pham).data, status=status.HTTP_201_CREATED)



    # API lấy sản phẩm của cửa hàng của người dùng
    @action(methods=['get'], detail=False, url_path='my-products')
    def my_products(self, request):
        user = request.user
        store = CuaHang.objects.filter(chu_so_huu=user).first()

        if not store:
            return Response({'detail': 'Bạn chưa có cửa hàng'}, status=status.HTTP_404_NOT_FOUND)

        products = SanPham.objects.filter(cua_hang=store, active=True)
        return Response(SanPhamSerializer(products, many=True).data)

    # API cập nhật sản phẩm
    def partial_update(self, request, *args, **kwargs):
        user = request.user  # Lấy thông tin người dùng

        # Lấy sản phẩm cần sửa
        try:
            san_pham = SanPham.objects.get(id=kwargs['pk'])
        except SanPham.DoesNotExist:
            return Response({'detail': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra quyền sửa sản phẩm
        if san_pham.cua_hang.chu_so_huu != user:
            return Response({'detail': 'Bạn không có quyền sửa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        # Cập nhật sản phẩm
        serializer = self.get_serializer(san_pham, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API xóa sản phẩm
    def destroy(self, request, *args, **kwargs):
        user = request.user  # Lấy thông tin người dùng

        # Lấy sản phẩm cần xóa
        try:
            san_pham = SanPham.objects.get(id=kwargs['pk'])
        except SanPham.DoesNotExist:
            return Response({'detail': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra quyền xóa sản phẩm
        if san_pham.cua_hang.chu_so_huu != user:
            return Response({'detail': 'Bạn không có quyền xóa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        san_pham.delete()
        return Response({'detail': 'Sản phẩm đã được xóa thành công'}, status=status.HTTP_204_NO_CONTENT)
    # Liệt kê các sản phẩm với các bộ lọc và sắp xếp
    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        # Tìm kiếm theo tên sản phẩm
        ten = request.query_params.get('ten')
        if ten:
            queryset = queryset.filter(ten__icontains=ten)

        # Lọc theo khoảng giá
        gia_min = request.query_params.get('gia_min')
        gia_max = request.query_params.get('gia_max')
        if gia_min and gia_max:
            queryset = queryset.filter(gia__gte=gia_min, gia__lte=gia_max)
        elif gia_min:
            queryset = queryset.filter(gia__gte=gia_min)
        elif gia_max:
            queryset = queryset.filter(gia__lte=gia_max)

        # Tìm kiếm theo tên cửa hàng
        cua_hang_ten = request.query_params.get('cua_hang')
        if cua_hang_ten:
            queryset = queryset.filter(cua_hang__ten__icontains=cua_hang_ten)

        # Sắp xếp theo tên hoặc giá
        ordering = request.query_params.get('ordering')
        if ordering in ['ten', '-ten', 'gia', '-gia']:
            queryset = queryset.order_by(ordering)

        # Trả về kết quả không phân trang
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # So sánh sản phẩm theo danh mục và tên sản phẩm
    @action(methods=['get'], detail=False, url_path='compare-products')
    def compare_products(self, request):
        danh_muc_id = request.query_params.get('danh_muc')
        ten_san_pham = request.query_params.get('ten_san_pham')

        # Kiểm tra nếu không có thông tin cần thiết
        if not danh_muc_id or not ten_san_pham:
            return Response({'detail': 'Vui lòng cung cấp danh mục và tên sản phẩm'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            danh_muc = DanhMuc.objects.get(id=danh_muc_id)  # Lấy danh mục
        except DanhMuc.DoesNotExist:
            return Response({'detail': 'Danh mục không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

        # Lọc sản phẩm theo danh mục và tên
        san_pham_list = SanPham.objects.filter(danh_muc=danh_muc, ten__icontains=ten_san_pham, active=True)

        if not san_pham_list.exists():
            return Response({'detail': 'Không tìm thấy sản phẩm phù hợp'}, status=status.HTTP_404_NOT_FOUND)

        result = []
        for san_pham in san_pham_list:
            # Tính điểm đánh giá trung bình của sản phẩm
            avg_rating = san_pham.danh_gia_san_pham.aggregate(Avg('diem'))['diem__avg'] or 0
            result.append({
                'ten': san_pham.ten,
                'gia': san_pham.gia,
                'so_luong_ton': san_pham.so_luong_ton,
                'cua_hang': san_pham.cua_hang.ten,
                'danh_gia_trung_binh': round(avg_rating, 2)
            })

        # Sắp xếp theo giá và đánh giá trung bình
        result.sort(key=lambda x: (x['gia'], -x['danh_gia_trung_binh']))

        return Response(result, status=status.HTTP_200_OK)

# ViewSet cho Giỏ hàng
class GioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    # Lấy tất cả giỏ hàng
    queryset = GioHang.objects.all()
    serializer_class = serializers.GioHangSerializer

    # Tạo giỏ hàng mới và thêm sản phẩm vào giỏ hàng
    def create(self, request, *args, **kwargs):
        user = request.user

        # Kiểm tra xem người dùng đã có giỏ hàng chưa, nếu chưa thì tạo mới
        gio_hang, created = GioHang.objects.get_or_create(nguoi_dung=user)

        # Lấy danh sách sản phẩm từ request
        product_data = request.data.get('san_pham', [])  # Danh sách sản phẩm (danh sách dict)

        # Lặp qua danh sách sản phẩm và thêm vào giỏ hàng
        for item in product_data:
            san_pham_id = item.get('san_pham')  # ID sản phẩm
            so_luong = item.get('so_luong', 1)  # Số lượng sản phẩm

            # Kiểm tra xem sản phẩm có tồn tại trong hệ thống không
            try:
                san_pham = SanPham.objects.get(id=san_pham_id)
            except SanPham.DoesNotExist:
                return Response({'detail': f'Sản phẩm {san_pham_id} không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra số lượng sản phẩm có đủ hay không
            if san_pham.so_luong_ton < so_luong:
                return Response({'detail': f'Số lượng sản phẩm {san_pham.ten} không đủ'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Thêm sản phẩm vào giỏ hàng
            SanPhamGioHang.objects.create(gio_hang=gio_hang, san_pham=san_pham, so_luong=so_luong, gia=san_pham.gia)

        # Cập nhật tổng tiền giỏ hàng
        gio_hang.tinh_tong_tien()

        return Response(serializers.GioHangSerializer(gio_hang).data, status=status.HTTP_201_CREATED)

    # Xóa sản phẩm trong giỏ hàng
    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Lấy sản phẩm trong giỏ hàng cần xóa
        try:
            san_pham_gio_hang = SanPhamGioHang.objects.get(id=kwargs['pk'])
        except SanPhamGioHang.DoesNotExist:
            return Response({'detail': 'Sản phẩm trong giỏ hàng không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem sản phẩm này có thuộc giỏ hàng của người dùng không
        if san_pham_gio_hang.gio_hang.nguoi_dung != user:
            return Response({'detail': 'Bạn không có quyền xóa sản phẩm này'}, status=status.HTTP_403_FORBIDDEN)

        # Xóa sản phẩm trong giỏ hàng
        san_pham_gio_hang.delete()

        # Cập nhật lại tổng tiền của giỏ hàng sau khi xóa sản phẩm
        san_pham_gio_hang.gio_hang.tinh_tong_tien()

        return Response({'detail': 'Sản phẩm đã được xóa khỏi giỏ hàng'}, status=status.HTTP_204_NO_CONTENT)

# ViewSet cho sản phẩm trong giỏ hàng
class SanPhamGioHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamGioHang.objects.all()
    serializer_class = serializers.SanPhamGioHangSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from stores.models import DonHang, SanPham, SanPhamDonHang, GioHang, ThongKeDoanhThu, ThongKeDonHangVaSanPhamCuaHang
from stores.serializers import DonHangSerializer
from django.shortcuts import get_object_or_404

class DonHangViewSet(viewsets.ModelViewSet):
    queryset = DonHang.objects.all()
    serializer_class = DonHangSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Users should only see their own orders.
        Admins see all orders.
        """
        user = self.request.user
        if user.is_staff or user.vai_tro == 'admin':
            return DonHang.objects.all()
        return DonHang.objects.filter(nguoi_dung=user)

    def create(self, request, *args, **kwargs):
        """
        Create an order either from:
        - A single product purchase (`san_pham`, `so_luong`)
        - The entire cart (`gio_hang`)
        """
        user = request.user
        product_data = request.data
        phuong_thuc_thanh_toan = product_data.get('phuong_thuc_thanh_toan')

        # ✅ Case 1: Direct Product Purchase
        if 'san_pham' in product_data and 'so_luong' in product_data:
            san_pham = get_object_or_404(SanPham, id=product_data.get('san_pham'))
            so_luong = int(product_data.get('so_luong', 1))

            if san_pham.so_luong_ton < so_luong:
                return Response({'detail': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Order
            don_hang = DonHang.objects.create(
                nguoi_dung=user,
                phuong_thuc_thanh_toan=phuong_thuc_thanh_toan,
                tong_tien=san_pham.gia * so_luong
            )

            # Add product to order
            SanPhamDonHang.objects.create(don_hang=don_hang, san_pham=san_pham, so_luong=so_luong, gia=san_pham.gia)

            # Update Sales Statistics
            ThongKeDoanhThu.objects.create(cua_hang=san_pham.cua_hang, danh_muc=san_pham.danh_muc,
                                           san_pham=san_pham, so_luong=so_luong, gia=san_pham.gia,
                                           ngay_thanh_toan=don_hang.ngay_tao,
                                           tong_doanh_thu=san_pham.gia * so_luong)

            return Response(DonHangSerializer(don_hang).data, status=status.HTTP_201_CREATED)

        # ✅ Case 2: Checkout Entire Cart
        gio_hang = get_object_or_404(GioHang, nguoi_dung=user)
        san_pham_gio_hang = gio_hang.san_pham.all()

        if not san_pham_gio_hang:
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        don_hang = DonHang.objects.create(
            nguoi_dung=user,
            phuong_thuc_thanh_toan=phuong_thuc_thanh_toan,
            tong_tien=gio_hang.tong_tien
        )

        for item in san_pham_gio_hang:
            SanPhamDonHang.objects.create(don_hang=don_hang, san_pham=item.san_pham, so_luong=item.so_luong, gia=item.gia)

            ThongKeDoanhThu.objects.create(cua_hang=item.san_pham.cua_hang, danh_muc=item.san_pham.danh_muc,
                                           san_pham=item.san_pham, so_luong=item.so_luong, gia=item.gia,
                                           ngay_thanh_toan=don_hang.ngay_tao, tong_doanh_thu=item.gia * item.so_luong)

        gio_hang.delete()

        return Response(DonHangSerializer(don_hang).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        """
        Allows a user to cancel an order if it's still pending.
        """
        don_hang = self.get_object()

        if don_hang.nguoi_dung != request.user:
            return Response({'detail': 'You cannot cancel this order'}, status=status.HTTP_403_FORBIDDEN)

        if don_hang.da_thanh_toan or don_hang.trang_thai != "pending":
            return Response({'detail': 'Only pending unpaid orders can be canceled'}, status=status.HTTP_400_BAD_REQUEST)

        don_hang.trang_thai = "canceled"
        don_hang.save()
        return Response({'message': 'Order canceled successfully'})


# ViewSet cho sản phẩm trong đơn hàng
class SanPhamDonHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SanPhamDonHang.objects.all()
    serializer_class = serializers.SanPhamDonHangSerializer

# ViewSet cho đánh giá sản phẩm
class DanhGiaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaSanPham.objects.all()
    serializer_class = serializers.DanhGiaSanPhamSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Tạo đánh giá sản phẩm
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def tao_danh_gia(self, serializer):
        san_pham_id = self.request.data.get('san_pham')
        san_pham = get_object_or_404(SanPham, id=san_pham_id)
        # Kiểm tra nếu người dùng đã mua sản phẩm mới được đánh giá
        serializer.save(nguoi_dung=self.request.user, san_pham=san_pham)

    # Cập nhật đánh giá sản phẩm
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cap_nhat_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaSanPham, pk=pk, nguoi_dung=request.user)
        serializer = self.get_serializer(danh_gia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa đánh giá sản phẩm
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def xoa_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaSanPham, pk=pk, nguoi_dung=request.user)
        danh_gia.delete()
        return Response({'message': 'Đã xoá đánh giá'}, status=status.HTTP_204_NO_CONTENT)

# ViewSet cho đánh giá người bán
class DanhGiaNguoiBanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DanhGiaNguoiBan.objects.all()
    serializer_class = serializers.DanhGiaNguoiBanSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Tạo đánh giá người bán
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def tao_danh_gia(self, serializer):
        nguoi_ban_id = self.request.data.get('nguoi_ban')
        nguoi_ban = get_object_or_404(CuaHang, id=nguoi_ban_id)
        serializer.save(nguoi_dung=self.request.user, nguoi_ban=nguoi_ban)

    # Cập nhật đánh giá người bán
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cap_nhat_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaNguoiBan, pk=pk, nguoi_dung=request.user)
        serializer = self.get_serializer(danh_gia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa đánh giá người bán
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def xoa_danh_gia(self, request, pk=None):
        danh_gia = get_object_or_404(DanhGiaNguoiBan, pk=pk, nguoi_dung=request.user)
        danh_gia.delete()
        return Response({'message': 'Đã xoá đánh giá'}, status=status.HTTP_204_NO_CONTENT)

# ViewSet cho tin nhắn
class TinNhanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TinNhan.objects.all()
    serializer_class = serializers.TinNhanSerializer

# ViewSet cho thống kê doanh thu
class ThongKeDoanhThuViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThongKeDoanhThu.objects.all()
    serializer_class = serializers.ThongKeDoanhThuSerializer

# ViewSet cho thống kê đơn hàng và sản phẩm của cửa hàng
class ThongKeDonHangVaSanPhamViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ThongKeDonHangVaSanPhamCuaHang.objects.all()
    serializer_class = serializers.ThongKeDonHangVaSanPhamSerializer
from rest_framework import viewsets
from stores.models import YeuCauXacMinh
from stores.serializers import YeuCauXacMinhSerializer
from rest_framework.permissions import IsAuthenticated

class YeuCauXacMinhViewSet(viewsets.ModelViewSet):
    queryset = YeuCauXacMinh.objects.all()
    serializer_class = YeuCauXacMinhSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import viewsets
from stores.models import ThanhToan
from stores.serializers import ThanhToanSerializer
from rest_framework.permissions import IsAuthenticated

class ThanhToanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling payments.
    """
    queryset = ThanhToan.objects.all()
    serializer_class = ThanhToanSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
from rest_framework import viewsets
from stores.models import SoSanhSanPham
from stores.serializers import SoSanhSanPhamSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class SoSanhSanPhamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for comparing products.
    """
    queryset = SoSanhSanPham.objects.all()
    serializer_class = SoSanhSanPhamSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    # Custom action to compare a product with similar ones
    @action(detail=True, methods=['get'])
    def compare(self, request, pk=None):
        try:
            product = SoSanhSanPham.objects.get(id=pk)
            similar_products = SoSanhSanPham.objects.filter(san_pham_goc=product.san_pham_goc)
            return Response(SoSanhSanPhamSerializer(similar_products, many=True).data)
        except SoSanhSanPham.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
from rest_framework import viewsets
from stores.models import KhoHang
from stores.serializers import KhoHangSerializer
from rest_framework.permissions import IsAuthenticated

class KhoHangViewSet(viewsets.ModelViewSet):
    """
    API endpoint for inventory management.
    """
    queryset = KhoHang.objects.all()
    serializer_class = KhoHangSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from stores.models import NguoiDung
from stores.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from stores.models import NguoiDung
from stores.serializers import UserSerializer
from rest_framework.authtoken.models import Token


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from stores.serializers import UserSerializer
from stores.serializers import StaffSerializer

from rest_framework.authtoken.models import Token
class AuthViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    @action(detail=False, methods=['post'], url_path='create-staff', url_name='create_staff')
    def create_staff(self, request):
        data = request.data
        staff_user = User.objects.create(
            username=data['username'],
            email=data['email'],
            vai_tro='staff'  # ✅ Ensure role is assigned
        )
        staff_user.set_password(data['password'])
        staff_user.save()

        serializer = StaffSerializer(staff_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Hash password

            if serializer.validated_data['vai_tro'] == 'seller':
                user.is_approved = False  # Requires admin approval
            else:
                user.is_approved = True
            
            user.save()
            return Response({
                "message": "User registered successfully",
                "is_approved": user.is_approved
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Login user and return token.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)  # Authenticate user properly
        
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_approved:
            return Response({"error": "Your account is pending approval."}, status=status.HTTP_403_FORBIDDEN)

        # Generate token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "username": user.username,
            "vai_tro": user.vai_tro,
            "access_token": token.key
        }, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from stores.models import DonHang, NguoiDung
from django.utils import timezone  # ✅ Add this import
from django.db import models  # ✅ Ensure models is also imported
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from stores.models import DonHang  # ✅ Ensure DonHang is imported
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stores.models import NguoiDung
from stores.serializers import NguoiDungSerializer
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=403)

    total_orders = DonHang.objects.count()
    monthly_sales = DonHang.objects.filter(
        ngay_tao__month=timezone.now().month
    ).aggregate(total=models.Sum("tong_tien"))["total"] or 0

    return Response({
        "total_orders": total_orders,
        "monthly_sales": monthly_sales,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_users(request):
    if not request.user.vai_tro == "admin":
        return Response({"error": "Only admins can access this."}, status=403)

    users = NguoiDung.objects.all()
    serializer = NguoiDungSerializer(users, many=True, context={"request": request})
    return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from stores.models import NguoiDung

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from stores.models import NguoiDung

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from stores.models import NguoiDung

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from stores.models import NguoiDung, CuaHang
from stores.serializers import CuaHangSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stores.models import NguoiDung, CuaHang
from stores.serializers import CuaHangSerializer
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])  # ✅ Ensure TokenAuthentication is used
@permission_classes([IsAuthenticated])  # ✅ Require authentication
def approve_seller(request, username):
    user = request.user

    # ✅ Check if user is an admin or staff
    if user.vai_tro not in ["admin", "staff"]:
        return Response({"error": "❌ Bạn không có quyền duyệt người bán!"}, status=403)

    try:
        seller = NguoiDung.objects.get(username=username, vai_tro="seller")
        seller.is_approved = True
        seller.save()

        # ✅ Auto-create store if seller is approved
        if not CuaHang.objects.filter(chu_so_huu=seller).exists():
            store = CuaHang.objects.create(
                chu_so_huu=seller,
                ten=f"Cửa hàng của {seller.username}",
                mo_ta="Cửa hàng được tạo tự động sau khi phê duyệt."
            )
            return Response({
                "message": f"✔ Người bán {username} đã được duyệt!",
                "store": CuaHangSerializer(store).data
            }, status=200)

        return Response({"message": f"✔ Người bán {username} đã được duyệt!"}, status=200)

    except NguoiDung.DoesNotExist:
        return Response({"error": "❌ Không tìm thấy người bán!"}, status=404)



@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_seller(request, username):  # ✅ Use username instead of id
    try:
        user = NguoiDung.objects.get(username=username, vai_tro="seller")
        user.delete()
        return Response({"message": f"Seller {username} deleted!"})
    except NguoiDung.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# stores/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from stores.models import ChatMessage, NguoiDung
from stores.serializers import ChatMessageSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    sender = request.user
    receiver_username = request.data.get("receiver")
    message_text = request.data.get("message")

    try:
        receiver = NguoiDung.objects.get(username=receiver_username)
        message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message_text)
        return Response({"message": "Message sent successfully!", "data": ChatMessageSerializer(message).data}, status=201)
    except NguoiDung.DoesNotExist:
        return Response({"error": "Receiver not found!"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, username):
    user = request.user
    try:
        other_user = NguoiDung.objects.get(username=username)
        messages = ChatMessage.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        ).order_by("created_at")

        return Response(ChatMessageSerializer(messages, many=True).data, status=200)
    except NguoiDung.DoesNotExist:
        return Response({"error": "User not found!"}, status=404)
