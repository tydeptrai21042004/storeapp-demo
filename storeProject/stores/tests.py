from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from stores.models import DonHang, SanPham, CuaHang

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        """Create default users for testing"""
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123", vai_tro="admin"
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="test123", vai_tro="user"
        )
        self.seller = User.objects.create_user(
            username="seller", email="seller@example.com", password="test123", vai_tro="seller"
        )

    def test_user_registration(self):
        """Test user registration"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "test123",
            "vai_tro": "user",
        }
        response = self.client.post("/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_user_login(self):
        """Test user login"""
        data = {"username": "testuser", "password": "test123"}
        response = self.client.post("/auth/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

class OrderTests(TestCase):
    def setUp(self):
        """Set up data for orders"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="buyer", email="buyer@example.com", password="buyer123", vai_tro="user"
        )
        self.seller = User.objects.create_user(
            username="storeowner", email="store@example.com", password="store123", vai_tro="seller"
        )
        self.store = CuaHang.objects.create(chu_so_huu=self.seller, ten="Store 1")
        self.product = SanPham.objects.create(
            cua_hang=self.store, ten="Product 1", gia=100, so_luong_ton=10
        )

    def test_create_order(self):
        """Test order creation"""
        self.client.force_authenticate(user=self.user)
        order_data = {
            "san_pham": self.product.id,
            "so_luong": 2,
            "phuong_thuc_thanh_toan": "cod",
        }
        response = self.client.post("/don-hang/", order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DonHang.objects.count(), 1)

class AdminTests(TestCase):
    def setUp(self):
        """Set up admin user"""
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123", vai_tro="admin"
        )
        self.client.force_authenticate(user=self.admin)

    def test_admin_statistics(self):
        """Test retrieving admin statistics"""
        response = self.client.get("/admin/stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
