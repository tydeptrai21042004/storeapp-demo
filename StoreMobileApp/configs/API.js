import axios from "axios";

// Define your Django backend base URL
const HOST = "http://127.0.0.1:8000";

export const endpoints = {
    "register": "/auth/register/",  // Correct registration endpoint
    "login": "/auth/login/",  // Authentication login
    "current-user": "/nguoi-dung/me/",  // Get current user

    // Other endpoints for your models
    "nguoi-dung": "/nguoi-dung/",
    "cua-hang": "/cua-hang/",
    "danh-muc": "/danh-muc/",
    "san-pham": "/san-pham/",
    "don-hang": "/don-hang/",
    "gio-hang": "/gio-hang/",
    "sanpham-giohang": "/sanpham-giohang/",
    "danhgia-sanpham": "/danhgia-sanpham/",
    "danhgia-nguoiban": "/danhgia-nguoiban/",
    "sanpham-donhang": "/sanpham-donhang/",
    "tin-nhan": "/tin-nhan/",
    "thongke-doanhthu": "/thongke-doanhthu/",
    "thongke-donhangsanpham": "/thongke-donhangsanpham/",
    "my-store": "/cua-hang/my-store/",
    "my-products": "/san-pham/my-products/",
    "add-product": "/san-pham/",
};

// Default API instance
const API = axios.create({
    baseURL: HOST,
    headers: {
        "Content-Type": "application/json",  // Ensure JSON data is accepted
        "Accept": "application/json"
    }
});

// Authenticated API requests (Requires token)

const BASE_URL = "http://127.0.0.1:8000";

export const authApi = (token) => {
    return axios.create({
      baseURL: BASE_URL,
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": token ? `Token ${token}` : "",  // ✅ Use `Token` instead of `Bearer`
        "Accept": "application/json",
      },
    });
};

  
  
  

// User Registration Function
export const registerUser = async (formData) => {
    try {
        const response = await API.post(endpoints["register"], formData, {
            headers: {
                "Content-Type": "multipart/form-data", // Ensure correct encoding
            },
        });

        return response.data;
    } catch (error) {
        console.error("Registration error:", error.response ? error.response.data : error);
        throw error;
    }
};




// Login Function
export const loginUser = async (username, password) => {
    try {
        const response = await API.post(
            endpoints["login"],
            { username, password },
            {
                headers: {
                    "Content-Type": "application/json", // Ensure JSON is sent
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error("Login failed:", error.response ? error.response.data : error);
        throw error;
    }
};


// Get current user
export const getCurrentUser = async (token) => {
    if (!token) {
        console.error("No token found, cannot fetch user.");
        throw new Error("No authentication token found");
    }

    try {
        const response = await axios.get(HOST + endpoints["current-user"], {
            headers: {
                "Authorization": `Token ${token}`,  // ✅ Fix: Use `Token` prefix (Django DRF default)
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching user:", error.response?.data || error);
        throw error;
    }
};



// Export API instance
export default API;
