import { use, useContext, useState } from 'react';
import { View, Text, TouchableOpacity, Alert, TextInput } from 'react-native';
import MyContext from '../../configs/MyContext';
import { loginUser, getCurrentUser } from '../../configs/API';

const Login = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [secureText, setSecureText] = useState(true);
  const [user, dispatch] = useContext(MyContext);

  const login = async () => {
    if (!username || !password) {
      Alert.alert("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu!");
      return;
    }
  
    setLoading(true);
    try {
      const data = await loginUser(username, password);
      console.log("Login successful:", data);
  
      dispatch({
        type: "login",
        payload: {
          username: data.username,
          role: data.vai_tro,
          token: data.access_token
        }
      });
  
      Alert.alert("Thành công", "Đăng nhập thành công!");
  
      // ✅ Ensure correct navigation
      if (data.vai_tro === 'admin' || data.vai_tro === 'staff') {
        navigation.reset({
          index: 0,
          routes: [{ name: "AdminDashboard" }],
        });
      } else if (data.vai_tro === 'seller') {
        navigation.reset({
          index: 0,
          routes: [{ name: "SellerDashboard" }],
        });
      } else {
        navigation.reset({
          index: 0,
          routes: [{ name: "Home" }],
        });
      }
    } catch (error) {
      Alert.alert("Lỗi", error.response?.data?.error || "Sai tên đăng nhập hoặc mật khẩu!");
      console.error("Login failed:", error);
    }
    setLoading(false);
  };
  

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 20 }}>Đăng Nhập</Text>
      
      <TextInput 
        value={username} 
        onChangeText={setUsername} 
        placeholder="Tên Đăng Nhập..." 
        style={{ borderWidth: 1, marginVertical: 10, padding: 10, borderRadius: 5 }} 
      />

      <View style={{ flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderRadius: 5, marginVertical: 10 }}>
        <TextInput 
          value={password} 
          onChangeText={setPassword} 
          secureTextEntry={secureText} 
          placeholder="Mật Khẩu..." 
          style={{ flex: 1, padding: 10 }} 
        />
        <TouchableOpacity onPress={() => setSecureText(!secureText)} style={{ padding: 10 }}>
          <Text>{secureText ? "👁" : "🙈"}</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity 
        onPress={login} 
        style={{ backgroundColor: loading ? 'gray' : 'blue', padding: 12, borderRadius: 5, marginTop: 10 }}
        disabled={loading}
      >
        <Text style={{ color: 'white', textAlign: 'center', fontSize: 16 }}>
          {loading ? "Đang đăng nhập..." : "Đăng Nhập"}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default Login;
