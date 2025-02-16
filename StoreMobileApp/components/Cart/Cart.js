import { useContext } from "react";
import { View, Text, FlatList, Button } from "react-native";
import MyContext from "../../configs/MyContext";

const Cart = ({ navigation }) => {
  const [user, dispatch] = useContext(MyContext);

  const removeItem = (id) => {
    dispatch({ type: "removeFromCart", payload: id });
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Giỏ hàng</Text>
      <FlatList
        data={user?.cart || []}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginVertical: 5 }}>
            <Text>{item.name} - ${item.price}</Text>
            <Button title="Xóa" onPress={() => removeItem(item.id)} />
          </View>
        )}
      />
      <Button title="Thanh toán" onPress={() => navigation.navigate("Payment")} />
    </View>
  );
};

export default Cart;
