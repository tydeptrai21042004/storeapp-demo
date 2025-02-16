import { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, Alert, Image, Picker } from "react-native";
import * as ImagePicker from "react-native-image-picker";
import { registerUser } from "../../configs/API";

const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const Register = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [avatar, setAvatar] = useState(null);
  const [vaiTro, setVaiTro] = useState("user"); // Default role
  const [loading, setLoading] = useState(false);

  const pickImage = () => {
    ImagePicker.launchImageLibrary({ mediaType: "photo" }, (response) => {
      if (response.didCancel) {
        console.log("User cancelled image picker");
      } else if (response.error) {
        console.log("ImagePicker Error: ", response.error);
      } else {
        const asset = response.assets[0];
        const fileType = asset.uri.split(".").pop();
        const mimeType = `image/${fileType}`;
        console.log("📤 Picked Image:", asset);
  
        setAvatar({
          uri: asset.uri,
          type: mimeType,
          name: `avatar.${fileType}`,
        });
      }
    });
  };
  


    const handleRegister = async () => {
      if (!username || !email || !password || !confirmPassword || !avatar) {
          Alert.alert("Lỗi", "Vui lòng nhập đầy đủ thông tin và chọn ảnh đại diện!");
          return;
      }
  
      if (!isValidEmail(email.trim())) {
          Alert.alert("Lỗi", "Email không hợp lệ!");
          return;
      }
  
      if (password !== confirmPassword) {
          Alert.alert("Lỗi", "Mật khẩu xác nhận không khớp!");
          return;
      }
  
      setLoading(true);
      try {
          const formData = new FormData();
          formData.append("username", username.trim());
          formData.append("email", email.trim().toLowerCase());
          formData.append("password", password);
          formData.append("vai_tro", vaiTro.trim());
          formData.append("avatar", avatar); // Sử dụng ảnh với type linh hoạt
  
          console.log("📤 Sending Form Data:", formData);
  
          await registerUser(formData);
          Alert.alert("Thành công", vaiTro === "seller" ? "Chờ xác nhận từ quản trị viên." : "Tạo tài khoản thành công!");
          navigation.navigate("Login");
      } catch (error) {
          let errorMessage = "Đăng ký thất bại! Hãy thử lại.";
          console.log("⚠️ Error:", error);
          Alert.alert("Lỗi", errorMessage);
      }
      setLoading(false);
  };
  




  return (
    <View style={{ padding: 20, alignItems: "center" }}>
      <Text style={{ fontSize: 20, fontWeight: "bold" }}>Đăng Ký</Text>

      {avatar && (
        <Image source={avatar} style={{ width: 100, height: 100, borderRadius: 50, marginVertical: 10 }} />
      )}
      <TouchableOpacity onPress={pickImage} style={{ backgroundColor: "gray", padding: 10, marginBottom: 10 }}>
        <Text style={{ color: "white", textAlign: "center" }}>Chọn Ảnh Đại Diện</Text>
      </TouchableOpacity>

      <TextInput value={username} onChangeText={setUsername} placeholder="Tên Đăng Nhập" style={{ borderWidth: 1, marginVertical: 10, padding: 8, width: "100%" }} />
      <TextInput value={email} onChangeText={setEmail} placeholder="Email" style={{ borderWidth: 1, marginVertical: 10, padding: 8, width: "100%" }} />
      <TextInput value={password} onChangeText={setPassword} secureTextEntry={true} placeholder="Mật Khẩu" style={{ borderWidth: 1, marginVertical: 10, padding: 8, width: "100%" }} />
      <TextInput value={confirmPassword} onChangeText={setConfirmPassword} secureTextEntry={true} placeholder="Xác Nhận Mật Khẩu" style={{ borderWidth: 1, marginVertical: 10, padding: 8, width: "100%" }} />

      <Picker selectedValue={vaiTro} onValueChange={(itemValue) => setVaiTro(itemValue)} style={{ height: 50, width: "100%", marginVertical: 10 }}>
        <Picker.Item label="Người dùng cá nhân" value="user" />
        <Picker.Item label="Người bán hàng (Yêu cầu xác nhận)" value="seller" />
      </Picker>

      <TouchableOpacity onPress={handleRegister} style={{ backgroundColor: loading ? "gray" : "blue", padding: 10, width: "100%" }}>
        <Text style={{ color: "white", textAlign: "center" }}>{loading ? "Đang đăng ký..." : "Đăng Ký"}</Text>
      </TouchableOpacity>
    </View>
  );
};

export default Register;
