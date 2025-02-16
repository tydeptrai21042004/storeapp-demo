import { createDrawerNavigator } from "@react-navigation/drawer";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import { useReducer } from "react";
import { StyleSheet } from "react-native";

import MyContext from "./configs/MyContext";
import MyUserReducer from "./reducers/MyUserReducer";
import Home from "./components/Home/Home";
import Login from "./components/User/Login";
import Register from "./components/User/Register";
import Logout from "./components/User/Logout";
import Profile from "./components/User/Profile";
import Cart from "./components/Cart/Cart";
import Payment from "./components/Cart/Payment";
import StoreManagement from "./components/Seller/StoreManagement";
import AdminDashboard from "./components/Admin/AdminDashboard";
import ChatScreen from "./components/Chat/ChatScreen";  // ✅ Import Chat

const Drawer = createDrawerNavigator();
const Tab = createBottomTabNavigator();

// ✅ User Dashboard (Regular Buyer)
const UserDashboard = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={Home} options={{ title: "Trang Chủ" }} />
      <Tab.Screen name="Profile" component={Profile} options={{ title: "Hồ Sơ Cá Nhân" }} />
      <Tab.Screen name="Cart" component={Cart} options={{ title: "Giỏ Hàng" }} />
      <Tab.Screen name="Payment" component={Payment} options={{ title: "Thanh Toán" }} />
      <Tab.Screen
        name="Chat"
        component={ChatScreen}
        options={{ title: "Chat Hỗ Trợ" }}
      />
    </Tab.Navigator>
  );
};

// ✅ Seller Dashboard
const SellerDashboard = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="StoreManagement" component={StoreManagement} options={{ title: "Quản Lý Cửa Hàng" }} />
      <Tab.Screen name="AdminDashboard" component={AdminDashboard} options={{ title: "Báo Cáo" }} />
      <Tab.Screen
        name="Chat"
        component={ChatScreen}
        options={{ title: "Tin Nhắn" }}
      />
    </Tab.Navigator>
  );
};

// ✅ Admin Dashboard
const AdminDrawer = () => {
  return (
    <Drawer.Navigator>
      <Drawer.Screen name="AdminDashboard" component={AdminDashboard} options={{ title: "Quản Trị" }} />
      <Drawer.Screen name="Chat" component={ChatScreen} options={{ title: "Hỗ Trợ Người Dùng" }} />
    </Drawer.Navigator>
  );
};

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);
  console.log("User state:", user);

  return (
    <MyContext.Provider value={[user, dispatch]}>
      <NavigationContainer>
        <Drawer.Navigator
          screenOptions={({ navigation }) => ({
            headerRight: () => <Logout navigation={navigation} />,
          })}
        >
          {user === null ? (
            <>
              <Drawer.Screen name="Login" component={Login} options={{ title: "Đăng Nhập" }} />
              <Drawer.Screen name="Register" component={Register} options={{ title: "Đăng Ký" }} />
            </>
          ) : user.role === "admin" ? (
            <Drawer.Screen name="Admin" component={AdminDrawer} options={{ title: "Quản Trị" }} />
          ) : user.role === "seller" ? (
            <Drawer.Screen name="SellerDashboard" component={SellerDashboard} options={{ title: "Khu Vực Bán Hàng" }} />
          ) : (
            <Drawer.Screen name="UserDashboard" component={UserDashboard} options={{ title: "Người Dùng" }} />
          )}
        </Drawer.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});

export default App;
