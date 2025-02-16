from stores.models import DanhMuc

# Create a new category with id=1
category, created = DanhMuc.objects.get_or_create(
    id=1, 
    ten="Danh mục mẫu",  # Change name if needed
    mo_ta="Đây là một danh mục test"  # Change description if needed
)

print("✅ Danh mục đã được tạo:", category, "Created:", created)
