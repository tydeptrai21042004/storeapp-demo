import { View, Text, Button, Image } from "react-native";
import { useContext, useState } from "react";
import MyContext from "../../configs/MyContext";
import API from "../../configs/API";

const Payment = () => {
  const [user] = useContext(MyContext);
  const [qrImage, setQrImage] = useState(null);

  const handlePayment = async (method) => {
    try {
      const res = await API.post("/payment/", { 
        user: user.id, 
        cart: user.cart, 
        method: method 
      });
      
      if (res.data.qrImage) {
        setQrImage(res.data.qrImage);
      } else {
        console.log("Payment successful, but no QR image provided:", res.data);
      }
    } catch (error) {
      console.error("Payment error:", error);
    }
  };

  return (
    <View style={{ padding: 20, alignItems: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Chọn phương thức thanh toán</Text>
      <Button title="Thanh toán với PayPal" onPress={() => handlePayment("PayPal")} />
      <Button title="Thanh toán với MoMo" onPress={() => handlePayment("MoMo")} />
      <Button title="Thanh toán với ZaloPay" onPress={() => handlePayment("ZaloPay")} />
      
      {qrImage && (
        <View style={{ marginTop: 20, alignItems: 'center' }}>
          <Text style={{ fontSize: 18, marginBottom: 10 }}>Quét mã QR để thanh toán</Text>
          <Image source={{ uri: qrImage }} style={{ width: 200, height: 200 }} />
        </View>
      )}
    </View>
  );
};

export default Payment;