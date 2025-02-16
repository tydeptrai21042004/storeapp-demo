import { useContext } from "react";
import { Button } from "react-native";
import { CommonActions } from "@react-navigation/native";  // ✅ Import reset function
import MyContext from "../../configs/MyContext";

const Logout = ({ navigation }) => {
    const [user, dispatch] = useContext(MyContext);

    const handleLogout = () => {
        dispatch({ type: "logout" });

        // ✅ Reset navigation to prevent back navigation issues
        navigation.dispatch(
            CommonActions.reset({
                index: 0,
                routes: [{ name: "Login" }],
            })
        );
    };

    if (user === null) {
        return <Button title="Đăng Nhập" onPress={() => navigation.navigate("Login")} />;
    }

    return <Button title="Đăng Xuất" onPress={handleLogout} />;
};

export default Logout;
