import { useEffect, useState, useContext } from "react";
import { View, Text, Button, FlatList, ActivityIndicator, Modal } from "react-native";
import { authApi, endpoints } from "../../configs/API";
import AddProductForm from "./AddProductForm";
import MyContext from "../../configs/MyContext"; // ✅ Import context

const StoreManagement = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [user] = useContext(MyContext); // ✅ Get user from context

  useEffect(() => {
    const loadProducts = async () => {
      if (!user?.token) {
        console.error("🚨 No token found! Cannot fetch products.");
        return;
      }
    
      console.log("🔍 Sending Token:", user.token); // Debug log
    
      try {
        let res = await authApi(user.token).get(endpoints["my-products"]);
        console.log("✅ Response:", res.data);
        setProducts(res.data);
      } catch (error) {
        console.error("🚨 Error loading store products:", error.response?.data || error);
      }
      setLoading(false);

    };
    

    loadProducts();
  }, [user]); // ✅ Depend on `user` instead of `token`

  const handleAddProduct = () => {
    setIsModalVisible(false);
    setLoading(true);
    
    // Reload the product list after adding a new product
    authApi(user.token)
      .get(endpoints["my-products"])
      .then((res) => setProducts(res.data))
      .finally(() => setLoading(false));
  };

  if (loading) {
    return <ActivityIndicator size="large" color="blue" />;
  }

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24 }}>Quản lý cửa hàng</Text>
      <FlatList
        data={products}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginVertical: 5 }}>
            <Text>{item.ten} - ${item.gia}</Text>
            <Button title="Sửa" onPress={() => console.log("Edit", item.id)} />
          </View>
        )}
      />
      <Button title="Thêm sản phẩm mới" onPress={() => setIsModalVisible(true)} />

      {/* Modal để thêm sản phẩm */}
      <Modal visible={isModalVisible} animationType="slide" transparent={true}>
        <View style={{ flex: 1, justifyContent: "center", backgroundColor: "rgba(0, 0, 0, 0.5)" }}>
          <View style={{ backgroundColor: "white", margin: 20, padding: 20 }}>
            <AddProductForm token={user.token} onAddProduct={handleAddProduct} />
            <Button title="Đóng" onPress={() => setIsModalVisible(false)} />
          </View>
        </View>
      </Modal>
    </View>
  );
};

export default StoreManagement;
