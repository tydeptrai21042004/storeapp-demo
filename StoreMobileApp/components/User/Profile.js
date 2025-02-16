import { useEffect, useState, useContext } from "react";
import { View, Text, TextInput, Button } from "react-native";
import { getCurrentUser, authApi } from "../../configs/API";
import MyContext from "../../configs/MyContext";

const Profile = () => {
  const [user, dispatch] = useContext(MyContext);
  const [profile, setProfile] = useState({ username: "", email: "" });
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    async function fetchUser() {
        if (!user || !user.token) {
            console.error("No token found, cannot fetch user.");
            return;
        }

        try {
            const data = await getCurrentUser(user.token);
            setProfile(data);
        } catch (error) {
            console.error("Failed to fetch user profile", error);
        }
    }
    fetchUser();
}, [user]);  // ✅ Depend on user state


  const updateProfile = async () => {
    try {
      await authApi(user.token).patch(`/nguoi-dung/${user.id}/update-profile/`, profile);
      alert("Profile updated!");
      setEditing(false);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View>
      <Text>Profile</Text>
      <TextInput value={profile.username} editable={editing} onChangeText={(text) => setProfile({ ...profile, username: text })} />
      <TextInput value={profile.email} editable={editing} onChangeText={(text) => setProfile({ ...profile, email: text })} />
      {editing ? (
        <Button title="Save" onPress={updateProfile} />
      ) : (
        <Button title="Edit" onPress={() => setEditing(true)} />
      )}
    </View>
  );
};

export default Profile;
