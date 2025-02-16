import { useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import API from "../../configs/API";

const ProductDetail = ({ route }) => {
  const { product } = route.params;
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState(product.comments || []);

  const postComment = async () => {
    try {
      const res = await API.post(`/san-pham/${product.id}/comment/`, { comment });
      setComments([...comments, res.data]);
      setComment("");
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>{product.name}</Text>
      <Text>Giá: ${product.price}</Text>
      <Text>{product.description}</Text>

      <TextInput
        placeholder="Nhập bình luận..."
        value={comment}
        onChangeText={setComment}
        style={{ borderWidth: 1, marginVertical: 10, padding: 8 }}
      />
      <Button title="Gửi bình luận" onPress={postComment} />

      <FlatList
        data={comments}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => <Text>{item.comment}</Text>}
      />
    </View>
  );
};

export default ProductDetail;
