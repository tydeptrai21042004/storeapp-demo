import { useEffect, useState, useContext } from "react";
import { View, Text, FlatList, TouchableOpacity, TextInput, Modal, Alert } from "react-native";
import { authApi } from "../../configs/API"; // ✅ Use authenticated API
import MyContext from "../../configs/MyContext";

const AdminDashboard = ({ navigation }) => {
  const [stats, setStats] = useState({});
  const [users, setUsers] = useState([]);
  const [pendingSellers, setPendingSellers] = useState([]);
  const [approvedSellers, setApprovedSellers] = useState([]);
  const [staffMembers, setStaffMembers] = useState([]);
  const [user] = useContext(MyContext); // ✅ Get current user from context
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [newStaff, setNewStaff] = useState({ username: "", email: "", password: "" });

  useEffect(() => {
    if (!user || (user.role !== "admin" && user.role !== "staff")) {  // ✅ Allow staff access
      console.warn("Unauthorized access! Redirecting...");
      navigation.replace("Login"); // ✅ Redirect non-admins
      return;
    }

    const loadStats = async () => {
      if (!user?.token) {
        console.error("🚨 No token found! Cannot fetch admin stats.");
        return;
      }

      try {
        console.log("🔑 Sending token:", user.token);
        const res = await authApi(user.token).get("/admin/stats/");
        setStats(res.data);
      } catch (error) {
        console.error("🚨 Error loading statistics:", error.response?.data || error);
      }
    };

    const loadUsers = async () => {
      try {
        let res = await authApi(user.token).get("/nguoi-dung/");
        console.log("✅ Raw API response:", res.data);

        const validUsers = res.data.filter(user => user.vai_tro && user.username);

        setUsers(validUsers.filter(user => user.vai_tro === "user"));
        setPendingSellers(validUsers.filter(user => user.vai_tro === "seller" && !user.is_approved));
        setApprovedSellers(validUsers.filter(user => user.vai_tro === "seller" && user.is_approved));
        setStaffMembers(validUsers.filter(user => user.vai_tro === "staff")); // ✅ Load staff members
      } catch (error) {
        console.error("🚨 Error loading users:", error.response?.data || error);
      }
    };

    loadStats();
    loadUsers();
    AdminDashboard.loadUsers = loadUsers;

  }, []);

  // ✅ Create Staff Function
  const createStaff = async () => {
    if (!newStaff.username || !newStaff.email || !newStaff.password) {
      Alert.alert("⚠ Lỗi", "Vui lòng nhập đầy đủ thông tin nhân viên!");
      return;
    }
  
    try {
      const staffData = { 
        ...newStaff, 
        vai_tro: "staff"  // ✅ Explicitly include role
      };
  
      const res = await authApi(user.token).post("/auth/create-staff/", staffData);
      
      // ✅ Ensure API response contains `vai_tro`
      if (!res.data.vai_tro) {
        throw new Error("API response is missing 'vai_tro' field.");
      }
  
      Alert.alert("✔ Thành công", `Nhân viên ${newStaff.username} đã được tạo!`);
      setIsModalVisible(false);
      setNewStaff({ username: "", email: "", password: "" });
  
      // ✅ Update state using API response
      setStaffMembers([...staffMembers, res.data]);
    } catch (error) {
      console.error("🚨 Error creating staff:", error.response?.data || error);
      Alert.alert("❌ Thất bại", "Không thể tạo nhân viên!");
    }
  };
  

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Admin Dashboard</Text>

      {/* 📊 Sales Statistics */}
      <Text style={{ marginTop: 10 }}>📈 Doanh thu tháng này: ${stats.monthly_sales || 0}</Text>
      <Text>📦 Tổng số đơn hàng: {stats.total_orders || 0}</Text>

      {/* 👥 User Management */}
      <Text style={{ marginTop: 20, fontWeight: "bold" }}>👤 Người dùng ({users.length})</Text>
      <FlatList
        data={users}
        keyExtractor={(item) => item.username}
        renderItem={({ item }) => (
          <Text>{item.username} ({item.email || "No email"})</Text>
        )}
      />

      {/* 🏪 Pending Sellers */}
      <Text style={{ marginTop: 20, fontWeight: "bold" }}>🛍️ Người bán chờ duyệt ({pendingSellers.length})</Text>
      <FlatList
        data={pendingSellers}
        keyExtractor={(item) => item.username}
        renderItem={({ item }) => (
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginVertical: 5 }}>
            <Text>{item.username} ({item.email || "No email"})</Text>
            <TouchableOpacity
              onPress={() => approveSeller(item.username, user, setPendingSellers, setApprovedSellers)}
              style={{ backgroundColor: "green", padding: 5, borderRadius: 5 }}
            >
              <Text style={{ color: "white" }}>✔ Duyệt</Text>
            </TouchableOpacity>
          </View>
        )}
      />

      {/* ✅ Approved Sellers */}
      <Text style={{ marginTop: 20, fontWeight: "bold" }}>✅ Người bán đã được duyệt ({approvedSellers.length})</Text>
      <FlatList
        data={approvedSellers}
        keyExtractor={(item) => item.username}
        renderItem={({ item }) => (
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginVertical: 5 }}>
            <Text>{item.username} ({item.email || "No email"})</Text>
            <TouchableOpacity
              onPress={() => deleteApprovedSeller(item.username, user, setApprovedSellers)}
              style={{ backgroundColor: "red", padding: 5, borderRadius: 5 }}
            >
              <Text style={{ color: "white" }}>✖ Hủy</Text>
            </TouchableOpacity>
          </View>
        )}
      />

      {/* 🛠 Staff Members */}
      <Text style={{ marginTop: 20, fontWeight: "bold" }}>🛠 Nhân viên ({staffMembers.length})</Text>
      <FlatList
        data={staffMembers}
        keyExtractor={(item) => item.username}
        renderItem={({ item }) => (
          <Text>{item.username} ({item.email || "No email"})</Text>
        )}
      />
      <TouchableOpacity
        onPress={() => setIsModalVisible(true)}
        style={{ backgroundColor: "blue", padding: 10, borderRadius: 5, marginTop: 10 }}
      >
        <Text style={{ color: "white", textAlign: "center" }}>➕ Thêm Nhân Viên</Text>
      </TouchableOpacity>

      {/* Modal to Create Staff */}
      <Modal visible={isModalVisible} animationType="slide" transparent={true}>
        <View style={{ flex: 1, justifyContent: "center", backgroundColor: "rgba(0, 0, 0, 0.5)" }}>
          <View style={{ backgroundColor: "white", margin: 20, padding: 20, borderRadius: 10 }}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>🛠 Thêm Nhân Viên</Text>

            <TextInput
              value={newStaff.username}
              onChangeText={(text) => setNewStaff({ ...newStaff, username: text })}
              placeholder="Tên đăng nhập"
              style={{ borderWidth: 1, marginVertical: 10, padding: 10, borderRadius: 5 }}
            />

            <TextInput
              value={newStaff.email}
              onChangeText={(text) => setNewStaff({ ...newStaff, email: text })}
              placeholder="Email"
              keyboardType="email-address"
              style={{ borderWidth: 1, marginVertical: 10, padding: 10, borderRadius: 5 }}
            />

            <TextInput
              value={newStaff.password}
              onChangeText={(text) => setNewStaff({ ...newStaff, password: text })}
              placeholder="Mật khẩu"
              secureTextEntry
              style={{ borderWidth: 1, marginVertical: 10, padding: 10, borderRadius: 5 }}
            />

            <TouchableOpacity onPress={createStaff} style={{ backgroundColor: "green", padding: 10, borderRadius: 5 }}>
              <Text style={{ color: "white", textAlign: "center" }}>✔ Tạo Nhân Viên</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => setIsModalVisible(false)} style={{ backgroundColor: "red", padding: 10, borderRadius: 5 }}>
              <Text style={{ color: "white", textAlign: "center" }}>✖ Hủy</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};
// ✅ Approve Seller Function
const approveSeller = async (username, user, setPendingSellers, setApprovedSellers) => {
  if (!username) {
    alert("⚠ Không tìm thấy tên người dùng!");
    return;
  }

  if (!user?.token) {
    console.error("🚨 No token found! Cannot approve seller.");
    alert("🚨 Lỗi: Token không hợp lệ!");
    return;
  }

  try {
    await authApi(user.token).patch(`/nguoi-dung/${username}/approve/`);
    alert(`✔ Người bán ${username} đã được duyệt!`);

    // ✅ Move the seller from pending to approved without reloading everything
    setPendingSellers((prev) => prev.filter((seller) => seller.username !== username));
    setApprovedSellers((prev) => [
      ...prev,
      { username, email: user.email, vai_tro: "seller", is_approved: true },
    ]);
  } catch (error) {
    console.error("🚨 Error approving seller:", error.response?.data || error);
  }
};



// ❌ Delete Approved Seller Function
const deleteApprovedSeller = async (username, user, setApprovedSellers) => {
  if (!username) {
    alert("⚠ Không tìm thấy tên người dùng!");
    return;
  }

  if (!user?.token) {
    alert("🚨 Lỗi: Token không hợp lệ!");
    return;
  }

  try {
    await authApi(user.token).delete(`/nguoi-dung/${username}/delete/`);
    alert(`✖ Người bán ${username} đã bị xóa khỏi hệ thống!`);

    // ✅ Remove from approved sellers without reloading everything
    setApprovedSellers((prev) => prev.filter((seller) => seller.username !== username));
  } catch (error) {
    console.error("🚨 Error deleting approved seller:", error.response?.data || error);
  }
};
export default AdminDashboard;
