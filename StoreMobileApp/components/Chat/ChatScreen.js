import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import { authApi } from "../../configs/API";  // ✅ Import authenticated API
import { useRoute } from "@react-navigation/native";

const ChatScreen = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState("");
  const route = useRoute();
  if (!route.params) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <Text>Error: Missing chat parameters!</Text>
      </View>
    );
  }
  //const { user, receiver } = route.params;
  const { user, receiver } = route.params || {}; // ✅ Prevents error when undefined

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const res = await authApi(user.token).get(`/chat/${receiver}/`);
      setMessages(res.data);
    } catch (error) {
      console.error("Error fetching messages:", error.response?.data || error);
    }
  };

  const sendMessage = async () => {
    if (!messageText.trim()) return;

    try {
      await authApi(user.token).post("/chat/send/", {
        receiver: receiver,
        message: messageText,
      });

      setMessageText("");
      fetchMessages(); // Refresh messages
    } catch (error) {
      console.error("Error sending message:", error.response?.data || error);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: "bold" }}>Chat with {receiver}</Text>

      <FlatList
        data={messages}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ marginVertical: 5, padding: 10, backgroundColor: item.sender === user.username ? "#DCF8C6" : "#EAEAEA" }}>
            <Text><b>{item.sender}:</b> {item.message}</Text>
          </View>
        )}
      />

      <TextInput
        value={messageText}
        onChangeText={setMessageText}
        placeholder="Type a message..."
        style={{ borderWidth: 1, padding: 10, marginTop: 10 }}
      />
      
      <Button title="Send" onPress={sendMessage} />
    </View>
  );
};

export default ChatScreen;
