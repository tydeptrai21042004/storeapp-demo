import { useState } from "react";
import { View, Text, TextInput, Button, Image, ActivityIndicator } from "react-native";
import * as ImagePicker from 'expo-image-picker';
import { authApi, endpoints } from "../../configs/API";

const AddProductForm = ({ token, onAddProduct }) => {
  const [ten, setTen] = useState("");
  const [mo_ta, setMoTa] = useState("");
  const [gia, setGia] = useState("");
  const [so_luong_ton, setSoLuongTon] = useState("");
  const [anh_san_pham, setAnhSanPham] = useState(null);
  const [loading, setLoading] = useState(false);
  const [danhMucId, setDanhMucId] = useState(""); // Stores user input category ID

  
  // Chọn ảnh từ thư viện hoặc máy ảnh
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });

    if (!result.canceled) {
      setAnhSanPham(result.assets[0].uri);
    }
  };

  const handleAddProduct = async () => {
    if (!ten || !mo_ta || !gia || !so_luong_ton || !danhMucId) {
      alert("Vui lòng điền đầy đủ thông tin và nhập ID danh mục!");
      return;
    }

    console.log("🔍 Token being used:", token); // Debug token
    console.log("🔍 Headers being sent:", {
        "Authorization": `Token ${token}`,
        "Content-Type": "multipart/form-data",
    });

    // ✅ Declare formData BEFORE using it
    const formData = new FormData();
    formData.append("ten", ten);
    formData.append("mo_ta", mo_ta);
    formData.append("gia", gia);
    formData.append("so_luong_ton", so_luong_ton);
    formData.append("danh_muc", parseInt(danhMucId, 10));  // ✅ Convert to integer
    console.log("🔍 Selected Category ID:", danhMucId);  // ✅ Check if the category ID is correct

    if (anh_san_pham) {
        let localUri = anh_san_pham;
        let filename = localUri.split("/").pop();
        let match = /\.(\w+)$/.exec(filename);
        let type = match ? `image/${match[1]}` : `image/jpeg`;

        formData.append("anh_san_pham", {
            uri: localUri,
            name: filename,
            type,
        });
    }

    try {
        setLoading(true);
        await authApi(token).post(endpoints["add-product"], formData, {
            headers: {
                "Authorization": `Token ${token}`,
           //     "Content-Type": "multipart/form-data",
            },
        });

        onAddProduct();
        alert("Sản phẩm đã được thêm thành công!");
    } catch (error) {
        console.error("🚨 Error adding product:", error.response?.data || error);
        alert("Có lỗi xảy ra, vui lòng thử lại!");
    } finally {
        setLoading(false);
    }
};

  
  

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24 }}>Thêm sản phẩm mới</Text>
      <TextInput
        style={{ marginVertical: 10, borderWidth: 1, padding: 10 }}
        placeholder="Tên sản phẩm"
        value={ten}
        onChangeText={setTen}
      />
      <TextInput
        style={{ marginVertical: 10, borderWidth: 1, padding: 10 }}
        placeholder="Mô tả sản phẩm"
        value={mo_ta}
        onChangeText={setMoTa}
      />
      <TextInput
        style={{ marginVertical: 10, borderWidth: 1, padding: 10 }}
        placeholder="Giá"
        keyboardType="numeric"
        value={gia}
        onChangeText={setGia}
      />
      <TextInput
        style={{ marginVertical: 10, borderWidth: 1, padding: 10 }}
        placeholder="Số lượng tồn"
        keyboardType="numeric"
        value={so_luong_ton}
        onChangeText={setSoLuongTon}
      />
      <TextInput
  style={{ marginVertical: 10, borderWidth: 1, padding: 10 }}
  placeholder="Nhập ID danh mục"
  keyboardType="numeric" // Ensures user enters a number
  value={danhMucId}
  onChangeText={setDanhMucId}
/>

      {/* Chọn ảnh sản phẩm */}
      <Button title="Chọn ảnh sản phẩm" onPress={pickImage} />
      {anh_san_pham && (
        <Image
          source={{ uri: anh_san_pham }}
          style={{ width: 100, height: 100, marginVertical: 10 }}
        />
      )}

      {/* Button thêm sản phẩm */}
      {loading ? (
        <ActivityIndicator size="large" color="blue" />
      ) : (
        <Button title="Thêm sản phẩm" onPress={handleAddProduct} />
      )}
    </View>
  );
};

export default AddProductForm;
