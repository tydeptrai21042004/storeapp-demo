import { useEffect, useState, useContext } from "react";
import { 
  View, Text, FlatList, TextInput, TouchableOpacity, Image, ScrollView, Button 
} from "react-native";
import API, { endpoints } from "../../configs/API";
import { useNavigation } from "@react-navigation/native";
import MyContext from "../../configs/MyContext";

const Home = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const [user] = useContext(MyContext);
  const navigation = useNavigation();

  useEffect(() => {
    loadProducts();
    loadCategories();
  }, [sortBy, selectedCategory]);

  // Fetch products
  const loadProducts = async () => {
    try {
      let url = endpoints["san-pham"] + `?ordering=${sortBy}`;
      if (selectedCategory) url += `&category=${selectedCategory}`;
      let res = await API.get(url);
      setProducts(res.data);
    } catch (error) {
      console.error("Error loading products:", error);
    }
  };

  // Fetch categories
  const loadCategories = async () => {
    try {
      let res = await API.get(endpoints["danh-muc"]);
      setCategories(res.data);
    } catch (error) {
      console.error("Error loading categories:", error);
    }
  };

  return (
    <View style={{ flex: 1, padding: 10, backgroundColor: "#f5f5f5" }}>
      
      {/* 🔥 Banner Slider */}
      <ScrollView horizontal pagingEnabled showsHorizontalScrollIndicator={false} style={{ height: 150, marginBottom: 15 }}>
        <Image source={{ uri: "https://via.placeholder.com/400x150" }} style={{ width: 400, height: 150 }} />
        <Image source={{ uri: "https://via.placeholder.com/400x150" }} style={{ width: 400, height: 150 }} />
        <Image source={{ uri: "https://via.placeholder.com/400x150" }} style={{ width: 400, height: 150 }} />
      </ScrollView>

      {/* 🔹 Search & Sorting */}
      <View style={{ flexDirection: "row", marginBottom: 10 }}>
        <TextInput 
          placeholder="🔍 Tìm kiếm sản phẩm..."
          value={search}
          onChangeText={setSearch}
          style={{ flex: 1, borderWidth: 1, padding: 8, borderRadius: 5, backgroundColor: "#fff" }}
        />
        <TouchableOpacity 
          onPress={() => setSortBy(sortBy === "price" ? "-price" : "price")} 
          style={{ marginLeft: 10, padding: 10, backgroundColor: "#ff8c00", borderRadius: 5 }}
        >
          <Text style={{ color: "#fff" }}>Sắp xếp</Text>
        </TouchableOpacity>
      </View>

      {/* 🔹 Categories */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: 10 }}>
        <TouchableOpacity 
          onPress={() => setSelectedCategory(null)} 
          style={{
            padding: 10,
            backgroundColor: selectedCategory ? "#ddd" : "#ff8c00",
            borderRadius: 5,
            marginRight: 5
          }}
        >
          <Text style={{ color: selectedCategory ? "#000" : "#fff" }}>Tất cả</Text>
        </TouchableOpacity>
        {categories.map((cat) => (
          <TouchableOpacity 
            key={cat.id} 
            onPress={() => setSelectedCategory(cat.id)}
            style={{
              padding: 10,
              backgroundColor: selectedCategory === cat.id ? "#ff8c00" : "#ddd",
              borderRadius: 5,
              marginRight: 5
            }}
          >
            <Text style={{ color: selectedCategory === cat.id ? "#fff" : "#000" }}>{cat.name}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* 🔹 Product Grid */}
      <FlatList
        data={products.filter(p => p.name.toLowerCase().includes(search.toLowerCase()))}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        columnWrapperStyle={{ justifyContent: "space-between" }}
        renderItem={({ item }) => (
          <TouchableOpacity 
            onPress={() => navigation.navigate("ProductDetail", { product: item })} 
            style={{
              flex: 1,
              backgroundColor: "#fff",
              borderRadius: 8,
              padding: 10,
              margin: 5,
              shadowColor: "#000",
              shadowOpacity: 0.2,
              shadowOffset: { width: 0, height: 1 },
              shadowRadius: 3,
              elevation: 2
            }}
          >
            {/* Product Image */}
            <Image 
              source={{ uri: item.anh_san_pham }} 
              style={{ width: "100%", height: 150, borderRadius: 5 }} 
              resizeMode="contain"
            />
            {/* Product Info */}
            <Text style={{ fontSize: 16, fontWeight: "bold", marginTop: 5 }}>{item.name}</Text>
            <Text style={{ color: "green", fontSize: 14, marginVertical: 5 }}>${item.price}</Text>
            <TouchableOpacity 
              style={{ backgroundColor: "#ff8c00", padding: 5, borderRadius: 5, marginTop: 5 }}
              onPress={() => console.log("Add to Cart", item.id)}
            >
              <Text style={{ textAlign: "center", color: "#fff" }}>🛒 Thêm vào giỏ</Text>
            </TouchableOpacity>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

export default Home;
